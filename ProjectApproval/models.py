#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 19:33
# Last modified: 2017-10-04 15:51
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from const.models import Workshop
from authentication.models import TeacherInfo
from . import PROJECT_STATUS, PROJECT_SUBMITTED
from . import ACTIVITY_RANGES, ACTIVITY_RANGE_WORKSHOP
from .utils import get_user_project_attachments_path


class Project(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, verbose_name=_('User'),
                             on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, verbose_name=_('Workshop'),
                                 on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name=('Project Status'),
                                 choices=PROJECT_STATUS,
                                 default=PROJECT_SUBMITTED)
    title = models.CharField(verbose_name=_('Project Title'), max_length=100)
    apply_time = models.DateTimeField(verbose_name=_('Apply Time'),
                                      auto_now_add=True)
    activity_time_from = models.DateTimeField(
        verbose_name=_('Activity Time From'))
    activity_time_to = models.DateTimeField(
        verbose_name=_('Activity Time To'))
    site = models.CharField(verbose_name=_('Site'), max_length=100)
    form = models.CharField(verbose_name=_('Project Form'), max_length=30)
    charger = models.CharField(verbose_name=_('Person in Charge'),
                               max_length=20)
    contact_info = models.CharField(verbose_name=_('Contact Info'),
                                    max_length=30)
    activity_range = models.IntegerField(verbose_name=_('Project Participant'),
                                         choices=ACTIVITY_RANGES,
                                         default=ACTIVITY_RANGE_WORKSHOP)
    amount = models.IntegerField(verbose_name=_('Participant Number'))
    has_social = models.BooleanField(verbose_name=_('Has Social'))
    budget = models.TextField(verbose_name=_('Budget Detail'))
    comment = models.TextField(verbose_name=_('Comment'))
    content = models.TextField(verbose_name=_('Project Content'), default='')
    attachment = models.FileField(
        verbose_name=_('Project Attachment'), blank=True,
        upload_to=get_user_project_attachments_path)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Project')
        default_permissions = ('add', 'delete', 'update', 'view')


class SocialInvitation(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    project = models.ForeignKey(Project, verbose_name=_('Project'),
                                on_delete=models.CASCADE)
    socials_info = models.TextField(verbose_name=_('Social List'))
    attend_info = models.TextField(verbose_name=_('Social Attend Info'))
    ideology_info = models.TextField(verbose_name=_('Social Ideology Info'))

    class Meta:
        verbose_name = _('Social Invitation')
        verbose_name_plural = _('Social Invitation')
        default_permissions = ('add', 'delete', 'update', 'view')
