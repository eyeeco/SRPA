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
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse, NoReverseMatch
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin

from ProjectApproval import PROJECT_STATUS, PROJECT_SUBMITTED
from ProjectApproval import PROJECT_SOCIALFORM_REQUIRED
from ProjectApproval import PROJECT_CANCELLED, PROJECT_END_SUBMITTED
from ProjectApproval import PROJECT_STATUS_CAN_END_SUBMIT
from ProjectApproval.forms import ActivityForm, SocialInvitationForm
from ProjectApproval.models import Project
from const.models import Workshop, FeedBack
from authentication.models import UserInfo
from authentication import USER_IDENTITIES
from authentication import USER_IDENTITY_STUDENT
from ProjectApproval import PROJECT_STATUS_CAN_EDIT
from ProjectApproval.utils import export_project
from tools.utils import assign_perms


class ProjectBase(UserPassesTestMixin):

    model = Project
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and\
            user.user_info.identity == USER_IDENTITY_STUDENT


class ProjectIndex(TemplateView):

    template_name = 'ProjectApproval/index.html'


class ProjectList(ProjectBase, PermissionListMixin, ListView):
    """
    A view for displaying user-related projects list. GET only.
    """
    paginate_by = 12
    ordering = ['status', '-apply_time']
    raise_exception = True
    permission_required = 'view_project'

    def get_queryset(self):
        return super(ProjectList, self).get_queryset().filter(
            user=self.request.user)


class ProjectDetail(ProjectBase, PermissionRequiredMixin, DetailView):
    """
    A view for displaying specified project. GET only.
    """
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    permission_required = 'view_project'
    raise_exception = True

    def get_context_data(self, **kwargs):
        feed = FeedBack.objects.filter(
            target_uid=self.object.uid)
        kwargs['feed'] = feed
        project = Project.objects.get(uid=self.object.uid)
        print(project.budget_set.all())
        return super(ProjectDetail, self).get_context_data(**kwargs)


class ProjectAdd(ProjectBase, PermissionRequiredMixin, CreateView):
    """
    A view for creating a new project.
    """
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
        kwargs['new_project'] = 1
        return super(CreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        has_social = form.cleaned_data['has_social']
        if has_social:
            form.instance.status = PROJECT_SOCIALFORM_REQUIRED
        self.object = form.save()
        assign_perms(self.info_name, self.request.user, self.object,
                     perms=['update', 'view'])
        assign_perms(self.info_name, self.object.workshop.group, self.object,
                     perms=['update', 'view'])
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return None


class ProjectSocialAdd(ProjectBase, PermissionRequiredMixin, CreateView):
    """
    A view for creating a information set for social people.
    """
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
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdate(ProjectBase, PermissionRequiredMixin, UpdateView):
    """
    A view for updating an exist project. Should check status before
    change, reject change if not match specified status.
    """
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
        allowed_status = self.object.status in PROJECT_STATUS_CAN_EDIT
        if not allowed_status:
            return HttpResponseForbidden()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_EDIT
        if not allowed_status:
            return HttpResponseForbidden()
        return super(ProjectUpdate, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
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
        return HttpResponseRedirect(self.get_success_url())


class ProjectExport(ProjectBase, PermissionRequiredMixin, DetailView):
    """
    A view for exporting project application
    """
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True
    permission_required = 'view_project'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(export_project(self.object))


class ProjectCancel(ProjectBase, PermissionRequiredMixin, DetailView):
    """
    A view for student to cancel the project application himself
    """
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


class ProjectEnd(ProjectBase, PermissionRequiredMixin, UpdateView):
    """
    A view for student to end the project application
    """
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
        allowed_status = self.object.status in PROJECT_STATUS_CAN_END_SUBMIT
        if not allowed_status:
            return HttpResponseForbidden()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_END_SUBMIT
        if not allowed_status:
            return HttpResponseForbidden()
        return super(ProjectEnd, self).post(request, *args,
                                            **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        return super(UpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object.status = PROJECT_END_SUBMITTED
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
