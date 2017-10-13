#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:06
# Last modified: 2017-10-12 10:05
# Filename: info_detail.py
# Description:
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView
from guardian.mixins import PermissionRequiredMixin

from authentication import USER_IDENTITY_STUDENT
from authentication.models import StudentInfo


class InfoDetailBase(PermissionRequiredMixin, DetailView):
    """
    A base view for displaying detail info.
    """

    http_method_names = ['get']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    raise_exception = True


class StudentInfoDetail(UserPassesTestMixin, InfoDetailBase):
    """
    A view for displaying student info.
    """

    model = StudentInfo
    fields = ['student_id', 'institute']
    template_name = 'authentication/student_info_detail.html'
    permission_required = 'view_studentinfo'
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and \
            user.user_info.identity == USER_IDENTITY_STUDENT
