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
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
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

    template_name = "ProjectApproval/index.html"


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
    template_name = 'ProjectApproval/project_add.html'
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
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})


class ProjectUpdate(ProjectBase, UpdateView):
    """
    A view for updating an exist project. Should check status before
    change, reject change if not match specified status.
    """

    pass
