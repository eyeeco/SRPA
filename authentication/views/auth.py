#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:07
# Last modified: 2017-10-07 13:39
# Filename: auth.py
# Description:
import json

from django.views.generic import View, CreateView
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse, NoReverseMatch
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from authentication import USER_IDENTITY_STUDENT
from authentication.forms import StudentRegisterForm
from authentication.forms import LoginForm
from tools.utils import assign_perms


class IndexView(LoginRequiredMixin, TemplateView):
    """
    A index view, nothing done yet.
    """

    template_name = 'authentication/index.html'


class LoginView(_LoginView):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('auth:admin:index')
        return super(LoginView, self).get_success_url()


class CaptchaRefresh(View):
    """
    A view for handling Ajax captcha refresh request.
    """

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        response = {}
        response['key'] = CaptchaStore.generate_key()
        response['img'] = captcha_image_url(response['key'])
        return HttpResponse(json.dumps(response),
                            content_type='application/json')


class StudentRegisterView(CreateView):
    """
    A view for student registration.
    """

    template_name = 'authentication/register.html'
    form_class = StudentRegisterForm
    success_url = reverse_lazy('index')
    identity = USER_IDENTITY_STUDENT
    form_post_url = reverse_lazy('auth:register:index')
    info_name = 'studentinfo'

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
        login(self.request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        self.object = form.save()
        assign_perms(self.info_name, user, self.object,
                     perms=['update', 'view'])
        # Assign perm to add Project and Reservation
        assign_perms('reservation', user, perms='add',
                     app_name='SiteReservation')
        assign_perms('project', user, perms='add',
                     app_name='ProjectApproval')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['identity'] = self.identity
        return super(StudentRegisterView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('index'), permanent=True)
        return super(StudentRegisterView, self).get(request, *args, **kwargs)
