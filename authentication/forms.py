#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:09
# Last modified: 2017-09-25 17:26
# Filename: forms.py
# Description:
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from const.models import CaptchaField
from .models import UserInfo, StudentInfo
from .allow_ids import ALLOW_IDS


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()


class RegisterForm(ModelForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput())
    name = forms.CharField(
        label='姓名',
        widget=forms.TextInput())
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(),
        min_length=1,
        max_length=20)
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(),
        min_length=1,
        max_length=20)
    phone = forms.CharField(
        label='联系电话',
        widget=forms.TextInput(),
        min_length=11,
        max_length=11)
    captcha = CaptchaField()

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'confirm_password',
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
            errors['username'] = ['该用户名已被使用']
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            errors['confirm_password'] = ['请确认两次输入密码一致']
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class StudentRegisterForm(RegisterForm):
    class Meta:
        model = StudentInfo
        fields = ['username', 'password', 'confirm_password',
                  'name', 'phone', 'student_id', 'institute', 'captcha']

    def clean_student_id(self, *args, **kwargs):
        student_id = self.cleaned_data['student_id']
        if student_id not in ALLOW_IDS:
            raise forms.ValidationError('学号不在受邀注册名单内')
        return student_id
