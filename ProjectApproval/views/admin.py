#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:17
# Last modified: 2017-10-04 15:46
# Filename: admin.py
# Description:
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _

from const.forms import FeedBackForm
from const.models import FeedBack
from ProjectApproval.models import Project
from ProjectApproval import PROJECT_STATUS_CAN_CHECK, PROJECT_SUBMITTED
from ProjectApproval import PROJECT_APPROVED, PROJECT_EDITTING
from ProjectApproval import PROJECT_TERMINATED
from .ordinary import ProjectList, ProjectUpdate, ProjectDetail


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class AdminProjectBase(LoginRequiredMixin):
    """
    A base view for all project actions. SHOULD NOT DIRECTLY USE THIS.
    """
    model = Project


class AdminProjectList(AdminProjectBase, ProjectList):
    """
    A view for displaying projects list for admin. GET only.
    """
    ordering = ['status', '-apply_time']

    def get_queryset(self):
        teacher = self.request.user.user_info.teacher_info
        return super(ProjectList, self).get_queryset().filter(
            workshop=teacher.workshop_set.all()[0])


class AdminProjectDetail(AdminProjectBase, ProjectDetail):
    """
    A view for displaying specified project for admin. GET only.
    """
    def get_context_data(self, **kwargs):
        form = FeedBackForm({'target_uid': self.object.uid})
        kwargs['form'] = form
        return super(AdminProjectDetail, self).get_context_data(**kwargs)


class AdminProjectUpdate(AdminProjectBase, UpdateView):
    """
    A view for admin to update an exist project.
    Should check status before change, reject change if not match
    specified status.
    """
    http_method_names = ['post']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = FeedBackForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in PROJECT_STATUS_CAN_CHECK
        if not allowed_status:
            return HttpResponseForbidden()
        return super(AdminProjectUpdate, self).post(request, *args,
                                                    **kwargs)

    def get_form_kwargs(self):
        return {'data': self.request.POST}

    def form_valid(self, form):
        obj = self.object
        feedback = form.save(commit=False)
        if obj.uid != feedback.target_uid:
            # Mismatch target_uid
            return JsonResponse({'status': 2, 'reason': _('Illegal Input')})
        if obj.workshop.instructor.user_info.user != self.request.user:
            # Mismatch current teacher
            return JsonResponse({'status': 2, 'reason': _('Illegal Input')})
        feedback.user = self.request.user
        status = form.cleaned_data['status']
        if status == 'APPROVE':
            obj.status = PROJECT_APPROVED
        elif status == 'EDITTING':
            obj.status = PROJECT_EDITTING
        elif status == 'TERMINATED':
            obj.status = PROJECT_TERMINATED
        obj.save()
        feedback.save()
        return JsonResponse({'status': 0})

    def form_invalid(self, form):
        return JsonResponse({'status': 1, 'reason': _('Illegal Input')})
