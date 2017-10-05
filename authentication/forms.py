#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:09
# Last modified: 2017-10-04 21:41
# Filename: forms.py
# Description:
from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from const.models import CaptchaField
from .models import UserInfo, StudentInfo
from .allow_ids import ALLOW_IDS


class LoginForm(AuthenticationForm):
    captcha = CaptchaField(label=_('Captcha'))


class RegisterForm(ModelForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput())
    name = forms.CharField(
        label=_('First Name'),
        widget=forms.TextInput())
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(),
        min_length=1,
        max_length=20)
    confirm_password = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(),
        min_length=1,
        max_length=20)
    phone = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(),
        min_length=11,
        max_length=11)
    email = forms.EmailField(
        label=_('Email'))
    captcha = CaptchaField(label=_('Captcha'))

    class Meta:
        model = UserInfo
        fields = ['email', 'username', 'password', 'confirm_password',
                  'name', 'phone', 'captcha']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        errors = {}
        username = cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            errors['username'] = [_('Username has been used')]
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            errors['confirm_password'] = [
                _('Please confirm the password is the same')]
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class StudentRegisterForm(RegisterForm):
    class Meta:
        model = StudentInfo
        fields = ['email', 'username', 'password', 'confirm_password',
                  'name', 'phone', 'student_id', 'institute', 'captcha']

    def clean_student_id(self, *args, **kwargs):
        student_id = self.cleaned_data['student_id']
        if not settings.DEBUG and student_id not in ALLOW_IDS:
            raise forms.ValidationError(
                _('Student ID not in the invited list'))
        return student_id
