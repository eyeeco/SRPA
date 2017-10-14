#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:06
# Last modified: 2017-10-12 12:12
# Filename: info_update.py
# Description:
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from guardian.mixins import PermissionRequiredMixin

from authentication import USER_IDENTITY_STUDENT
from authentication.models import StudentInfo
from authentication.forms import StudentUpdateForm


class InfoUpdateBase(PermissionRequiredMixin, UpdateView):
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


class StudentInfoUpdate(UserPassesTestMixin, InfoUpdateBase):
    """
    A view for updaing student info.
    """

    model = StudentInfo
    form_class = StudentUpdateForm
    permission_required = 'update_studentinfo'
    form_post_url = 'auth:info:update:student'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and \
            user.user_info.identity == USER_IDENTITY_STUDENT

    def get_context_data(self, **kwargs):
        kwargs['back_url'] = reverse_lazy('auth:info:student',
                                          args=(self.object.uid,))
        return super(StudentInfoUpdate, self).get_context_data(**kwargs)

    def get_initial(self):
        kwargs = {}
        kwargs['name'] = self.request.user.first_name
        kwargs['email'] = self.request.user.email
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        user = self.request.user
        user.first_name = cleaned_data['name']
        user.email = cleaned_data['email']
        user.save()
        return super(StudentInfoUpdate, self).form_valid(form)
