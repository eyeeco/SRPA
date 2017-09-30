#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 18:34
# Last modified: 2017-09-22 09:52
# Filename: models.py
# Description:
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from captcha.fields import CaptchaField as _CaptchaField

from authentication.models import TeacherInfo


class Site(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name='场地', max_length=50)

    class Meta:
        verbose_name = '场地信息'
        verbose_name_plural = '场地信息'
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.desc


class Workshop(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name='工坊', max_length=50)
    instructor = models.ForeignKey(TeacherInfo, verbose_name='指导教师',
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = '工坊信息'
        verbose_name_plural = '工坊信息'
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.desc


class FeedBack(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, verbose_name='审阅人',
                             on_delete=models.CASCADE)
    target_uid = models.UUIDField(verbose_name='被审阅对象')
    created = models.DateTimeField(verbose_name='审阅时间', auto_now_add=True)
    desc = models.TextField(verbose_name='意见')

    class Meta:
        verbose_name = '审阅意见'
        verbose_name_plural = '审阅意见'

    def __str__(self):
        return '{}对{}的审阅意见'.format(self.user, self.target_uid)


class CaptchaField(_CaptchaField):
    def __init__(self, *args, **kwargs):
        super(CaptchaField, self).__init__(*args, **kwargs)
        self.label = '验证码'
