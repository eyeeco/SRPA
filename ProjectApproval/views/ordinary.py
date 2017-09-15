#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:17
# Last modified: 2017-09-09 10:08
# Filename: ordinary.py
# Description:
from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse, NoReverseMatch
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404

from ProjectApproval import PROJECT_STATUS, PROJECT_SUBMITTED
from ProjectApproval.forms import AddActivityForm
from ProjectApproval.models import Project
from const.models import Workshop
from authentication.models import TeacherInfo


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class ProjectBase(LoginRequiredMixin):
    """
    A base view for all project actions. SHOULD NOT DIRECTLY USE THIS.
    """
    model = Project


class ProjectIndex(ProjectBase, TemplateView):

    template_name = "ProjectApproval/base.html"


class ProjectRedirect(ProjectBase, RedirectView):
    """
    A view for redirect admin users and ordinary users.
    """
    def get(self, request, *args, **kwargs):
        register_type = request.GET.get('type', None)
        if register_type is None:
            raise Http404()
        try:
            self.url = reverse(register_type)
        except NoReverseMatch:
            raise Http404()
        return super(ProjectRedirect, self).get(request, *args, **kwargs)


class ProjectList(ProjectBase, ListView):
    """
    A view for displaying user-related projects list. GET only.
    """
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ProjectDetail(ProjectBase, DetailView):
    """
    A view for displaying specified project. GET only.
    """
    fields = ['title', 'workshop', 'activity_time_from',
              'activity_time_to', 'site', 'form', 'charger',
              'contact_info', 'activity_range', 'amount', 'has_social',
              'budget', 'comment', 'instructor_comment',
              'attachment']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class ProjectAdd(ProjectBase, CreateView):
    """
    A view for creating a new project.
    """
    form_class = AddActivityForm
    success_url = reverse_lazy('project:index')
    form_post_url = reverse_lazy('project:ordinary:add')

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.success_url
        return super(CreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdate(ProjectBase, UpdateView):
    """
    A view for updating an exist project. Should check status before
    change, reject change if not match specified status.
    """

    pass
