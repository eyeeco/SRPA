#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:17
# Last modified: 2017-10-05 10:01
# Filename: ordinary.py
# Description:
from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse, NoReverseMatch
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import PermissionRequiredMixin as dj_PRM
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin

from ProjectApproval import PROJECT_STATUS, PROJECT_SUBMITTED
from ProjectApproval import PROJECT_SOCIALFORM_REQUIRED
from ProjectApproval import PROJECT_CANCELLED, PROJECT_END_SUBMITTED
from ProjectApproval import PROJECT_STATUS_CAN_ENDED
from ProjectApproval.forms import ActivityForm, SocialInvitationForm
from ProjectApproval.models import Project
from const.models import Workshop, FeedBack
from authentication.models import UserInfo
from authentication import USER_IDENTITIES
from ProjectApproval import PROJECT_STATUS_CAN_EDIT
from ProjectApproval.utils import export_project
from tools.utils import assign_perms


class ProjectIndex(TemplateView):

    template_name = "ProjectApproval/index.html"


class ProjectList(PermissionListMixin, ListView):
    """
    A view for displaying user-related projects list. GET only.
    """
    model = Project
    paginate_by = 12
    ordering = ['status', '-apply_time']
    raise_exception = True
    permission_required = 'view_project'
    def get_queryset(self):
        return super(ProjectList,self).get_queryset().filter(user=self.request.user)


class ProjectDetail(PermissionRequiredMixin, DetailView):
    """
    A view for displaying specified project. GET only.
    """
    model = Project
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    permission_required = 'view_project' 
    raise_exception = True 

    def get_context_data(self, **kwargs):
        feed = FeedBack.objects.filter(
            target_uid=self.object.uid)
        
        kwargs['budgets'] = [x.strip().split(' ') for x in
                             self.object.budget.split('\n')]
        kwargs['feed'] = feed
        return super(ProjectDetail, self).get_context_data(**kwargs)


class ProjectAdd(dj_PRM, CreateView):
    """
    A view for creating a new project.
    """
    model = Project
    template_name = 'ProjectApproval/project_form.html'
    form_class = ActivityForm
    success_url = reverse_lazy('project:index')
    form_post_url = 'project:ordinary:add'
    info_name = 'project'
    raise_exception = True
    accept_global_perms = True
    permission_required = 'ProjectApproval.add_project'

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = reverse(self.form_post_url)
        kwargs['back_url'] = self.success_url
        return super(CreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        has_social = form.cleaned_data['has_social']
        if has_social:
            form.instance.status = PROJECT_SOCIALFORM_REQUIRED
        self.object = form.save()
        assign_perms(self.info_name, self.request.user, self.object,
                     perms=['update', 'view', 'delete'])
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})


class ProjectSocialAdd(PermissionRequiredMixin, CreateView):
    """
    A view for creating a information set for social people.
    """
    model = Project
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    template_name = 'ProjectApproval/project_add_social.html'
    form_class = SocialInvitationForm
    success_url = reverse_lazy('project:index')
    raise_exception = True
    permission_required = 'update_project'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = SocialInvitationForm({'target_uid': kwargs['uid']})
        kwargs['form'] = form
        kwargs['uid'] = kwargs['uid']
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = reverse('project:ordinary:social_add',
                                          args=(kwargs['uid'],))
        kwargs['back_url'] = self.success_url
        return super(ProjectSocialAdd, self).get_context_data(**kwargs)

    def form_valid(self, form):
        project = Project.objects.filter(
            uid=form.cleaned_data['target_uid'])[0]
        if project.status == PROJECT_SOCIALFORM_REQUIRED:
            project.status = PROJECT_SUBMITTED
        else:
            return HttpResponseForbidden()
        form.instance.project = project
        self.object = form.save()
        project.save()
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    """
    A view for updating an exist project. Should check status before
    change, reject change if not match specified status.
    """
    model = Project
    template_name = 'ProjectApproval/project_form.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = ActivityForm
    success_url = reverse_lazy('project:index')
    form_post_url = 'project:ordinary:update'
    raise_exception = True
    permission_required = 'update_project'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_ajax = request.is_ajax()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_EDIT
        if not is_ajax or not allowed_status:
            return HttpResponseForbidden()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_EDIT
        if not allowed_status:
            return HttpResponseForbidden()
        return super(ProjectUpdate, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['back_url'] = self.success_url
        kwargs['form_post_url'] = reverse(self.form_post_url,
                                          kwargs={'uid': self.object.uid})
        return super(UpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        has_social = form.cleaned_data['has_social']
        project = Project.objects.filter(uid=form.instance.uid)[0]
        social_invitation = project.socialinvitation_set.all()
        if has_social:
            form.instance.status = PROJECT_SOCIALFORM_REQUIRED
        else:
            form.instance.status = PROJECT_SUBMITTED
            if social_invitation:
                social_invitation.delete()
        self.object = form.save()
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})


class ProjectExport(PermissionRequiredMixin, DetailView):
    """
    A view for exporting project application
    """
    model = Project
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True
    permission_required = 'view_project'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(export_project(self.object))


class ProjectCancel(PermissionRequiredMixin, DetailView):
    """
    A view for student to cancel the project application himself
    """
    model = Project
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    success_url = reverse_lazy('project:index')
    raise_exception = True
    permission_required = 'update_project'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = PROJECT_CANCELLED
        self.object.save()
        return redirect(self.success_url)

class ProjectEnd(PermissionRequiredMixin, UpdateView):
    """
    A view for student to end the project application 
    """
    model = Project
    template_name = 'ProjectApproval/project_end.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    success_url = reverse_lazy('project:index')
    form_post_url = 'project:ordinary:project_end'
    fields = ['attachment']
    raise_exception = True
    permission_required = 'update_project'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_ajax = request.is_ajax()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_ENDED
        if not is_ajax or not allowed_status:
            return HttpResponseForbidden()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_ENDED
        if not allowed_status:
            return HttpResponseForbidden()
        return super(ProjectEnd, self).post(request, *args,
                                                    **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['back_url'] = self.success_url
        kwargs['form_post_url'] = self.form_post_url
        return super(UpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object.status = PROJECT_END_SUBMITTED
        self.object.save()
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})
