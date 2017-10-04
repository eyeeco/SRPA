#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:09
# Last modified: 2017-10-04 14:42
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as _User

from . import USER_IDENTITIES, USER_IDENTITY_UNSET
from . import POLITICAL_STATUS, TEACHER_TITLE
from . import INSTITUTES, EDUCATION_BACKGROUNDS, EDUCATION_NONE


class UserInfo(models.Model):
    user = models.OneToOneField(_User, verbose_name=_('User'),
                                on_delete=models.CASCADE,
                                related_name='user_info')
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    identity = models.IntegerField(verbose_name=_('Identity'),
                                   choices=USER_IDENTITIES,
                                   default=USER_IDENTITY_UNSET)
    phone = models.CharField(verbose_name=_('Phone'), max_length=20)

    class Meta:
        verbose_name = _('UserInfo')
        verbose_name_plural = _('UserInfo')
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.user.first_name


class StudentInfo(UserInfo):
    user_info = models.OneToOneField(UserInfo, verbose_name=_('UserInfo'),
                                     on_delete=models.CASCADE,
                                     parent_link=True,
                                     related_name='student_info')
    student_id = models.CharField(verbose_name=_('Student ID'), max_length=20)
    institute = models.CharField(verbose_name=_('Institute'), max_length=10,
                                 choices=INSTITUTES,
                                 default=INSTITUTES[0][0])

    class Meta:
        verbose_name = _('StudentInfo')
        verbose_name_plural = _('StudentInfo')
        default_permissions = ('add', 'delete', 'update', 'view')


class TeacherInfo(UserInfo):
    user_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE,
                                     parent_link=True,
                                     related_name='teacher_info')
    title = models.IntegerField(verbose_name=_('Title'),
                                choices=TEACHER_TITLE,
                                default=TEACHER_TITLE[0][0])

    class Meta:
        verbose_name = _('TeacherInfo')
        verbose_name_plural = _('TeacherInfo')
        default_permissions = ('add', 'delete', 'update', 'view')

    def __str__(self):
        return self.user_info.user.username
