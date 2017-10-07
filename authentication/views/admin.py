#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-06 14:12
# Last modified: 2017-10-07 17:05
# Filename: admin.py
# Description:
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from const.models import Workshop
from authentication import USER_IDENTITY_TEACHER
from authentication.forms import TeacherRegisterForm, TeacherUpdateForm
from authentication.forms import WorkshopUpdateForm
from authentication.models import TeacherInfo
from tools.utils import assign_perms


class AdminBase(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_superuser


class AdminIndex(AdminBase, TemplateView):
    template_name = 'authentication/admin/index.html'


class AdminTeacherAdd(AdminBase, CreateView):
    template_name = 'authentication/admin/teacher_add.html'
    form_class = TeacherRegisterForm
    identity = USER_IDENTITY_TEACHER
    success_url = reverse_lazy('auth:admin:index')
    form_post_url = reverse_lazy('auth:admin:teacher:add')
    info_name = 'teacherinfo'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['name']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name)
        form.instance.user = user
        form.instance.identity = self.identity
        self.object = form.save()
        assign_perms(self.info_name, user, self.object,
                     perms=['update', 'view'])
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        return super(AdminTeacherAdd, self).get_context_data(**kwargs)


class AdminTeacherUpdate(AdminBase, UpdateView):
    model = TeacherInfo
    form_class = TeacherUpdateForm
    template_name = 'authentication/admin/teacher_info_update.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    success_url = reverse_lazy('auth:admin:teacher:list', args=(1,))

    def get_initial(self):
        kwargs = {}
        kwargs['first_name'] = self.object.user_info.user.first_name
        kwargs['phone'] = self.object.user_info.phone
        kwargs['email'] = self.object.user_info.user.email
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        cleaned_data = form.cleaned_data
        user_info = self.object.user_info
        user_info.phone = cleaned_data['phone']
        user_info.save()
        user = user_info.user
        user.email = cleaned_data['email']
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class AdminTeacherDetail(AdminBase, DetailView):
    model = TeacherInfo
    template_name = 'authentication/admin/teacher_info_detail.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class AdminTeacherList(AdminBase, ListView):
    model = TeacherInfo
    template_name = 'authentication/admin/teacher_info_list.html'
    paginate_by = 10
    ordering = 'user_info__user__first_name'


class AdminWorkshopAdd(AdminBase, CreateView):
    model = Workshop
    template_name = 'authentication/admin/workshop_add.html'
    fields = ['desc']
    success_url = reverse_lazy('auth:admin:workshop:list', args=(1,))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        group, status = Group.objects.get_or_create(name=self.object.desc)
        self.object.group = group
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AdminWorkshopUpdate(AdminBase, UpdateView):
    model = Workshop
    form_class = WorkshopUpdateForm
    template_name = 'authentication/admin/workshop_update.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    success_url = reverse_lazy('auth:admin:workshop:list', args=(1,))

    def get_initial(self):
        kwargs = {}
        kwargs['group_users'] = self.object.group.user_set.all()
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        group = self.object.group
        old_users = User.objects.filter(groups__name=group)
        for user in old_users:
            user.groups.remove(group)
        for user in cleaned_data['group_users']:
            user.groups.add(group)
        return super(AdminWorkshopUpdate, self).form_valid(form)


class AdminWorkshopDetail(AdminBase, DetailView):
    model = Workshop
    template_name = 'authentication/admin/workshop_detail.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super(AdminWorkshopDetail, self).get_context_data(**kwargs)
        context['group_users'] = self.object.group.user_set.all()
        return context


class AdminWorkshopList(AdminBase, ListView):
    model = Workshop
    template_name = 'authentication/admin/workshop_list.html'
    paginate_by = 10
    ordering = 'desc'
