#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:06
# Last modified: 2017-09-30 09:43
# Filename: info_update.py
# Description:
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from guardian.mixins import PermissionRequiredMixin

from authentication.models import StudentInfo


class InfoUpdateBase(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    A base view for updaing info.
    """

    template_name = 'authentication/update_info.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy(self.success_url)

    def get_context_data(self, **kwargs):
        slug_val = getattr(self.object, self.slug_field)
        kwargs['form_post_url'] = reverse_lazy(self.form_post_url,
                                               args=(slug_val,))
        return super(InfoUpdateBase, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(self.success_url)
        return super(InfoUpdateBase, self).get(request, *args, **kwargs)


class StudentInfoUpdate(InfoUpdateBase):
    """
    A view for updaing student info.
    """

    model = StudentInfo
    fields = ['institute']
    success_url = 'index'
    permission_required = 'update_studentinfo'
    form_post_url = 'auth:info:update:student'
