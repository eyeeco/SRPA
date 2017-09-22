#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:17
# Last modified: 2017-09-09 10:08
# Filename: admin.py
# Description:
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from ProjectApproval.models import Project
from .ordinary import ProjectList, ProjectUpdate, ProjectDetail
from const.forms import FeedBackForm
from django.http import JsonResponse, HttpResponseForbidden
from ProjectApproval import PROJECT_STATUS_CAN_CHECK, PROJECT_SUBMITTED
from ProjectApproval import PROJECT_APPROVED, PROJECT_EDITTING
from ProjectApproval import PROJECT_TERMINATED


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
            return JsonResponse({'status': 2, 'reason': '非法输入'})
        if obj.workshop.instructor.user_info.user != self.request.user:
            # Mismatch current teacher
            return JsonResponse({'status': 2, 'reason': '非法输入'})
        feedback.user = self.request.user
        status = form.cleaned_data['status']
        if status == 'APPROVE':
            conflict = 0
            if conflict:
                return JsonResponse({'status': 3,
                                     'reason': '当前时间段已存在预约'})
            obj.status = PROJECT_APPROVED
        elif status == 'EDITTING':
            obj.status = PROJECT_EDITTING
        elif status == 'TERMINATED':
            obj.status = PROJECT_TERMINATED
        obj.save()
        feedback.save()
        return JsonResponse({'status': 0})

    def form_invalid(self, form):
        return JsonResponse({'status': 1, 'reason': '无效输入'})
