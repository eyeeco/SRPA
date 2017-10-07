#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 18:34
# Last modified: 2017-10-05 08:34
# Filename: models.py
# Description:
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField as _CaptchaField

from authentication.models import TeacherInfo


class Site(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name=_('Site Description'), max_length=50)

    class Meta:
        verbose_name = _('Site')
        verbose_name_plural = _('Site')
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.desc


class Workshop(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    desc = models.CharField(verbose_name=_('Workshop Description'),
                            max_length=50)
    instructor = models.ForeignKey(TeacherInfo, verbose_name=_('Instructor'),
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Workshop')
        verbose_name_plural = _('Workshop')
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.desc


class FeedBack(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, verbose_name=_('Auditor'),
                             on_delete=models.CASCADE)
    target_uid = models.UUIDField(verbose_name=_('Audited Target'))
    created = models.DateTimeField(verbose_name=_('Audit Time'),
                                   auto_now_add=True)
    desc = models.TextField(verbose_name=_('Audit Opinion'))

    class Meta:
        verbose_name = _('Audit Feedback')
        verbose_name_plural = _('Audit Feedback')

    def __str__(self):
        return _('Audit Feedback on {target} by {user}').format(
            self.user, self.target_uid)


class CaptchaField(_CaptchaField):
    def __init__(self, label=_('Captcha'), *args, **kwargs):
        super(CaptchaField, self).__init__(*args, **kwargs)
        self.label = label
