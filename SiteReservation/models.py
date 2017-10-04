#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 19:21
# Last modified: 2017-10-04 15:06
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from const.models import Site, Workshop
from . import RESERVATION_STATUS, RESERVATION_SUBMITTED


class Reservation(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, verbose_name=_('User'),
                             on_delete=models.CASCADE)
    site = models.ForeignKey(Site, verbose_name=_('Site'),
                             on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, verbose_name=_('Workshop'),
                                 on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name=_('Status'),
                                 choices=RESERVATION_STATUS,
                                 default=RESERVATION_SUBMITTED)
    title = models.CharField(verbose_name=_('Project Title'),
                             max_length=100)
    activity_time_from = models.DateTimeField(
        verbose_name=_('Activity Time From'))
    activity_time_to = models.DateTimeField(
        verbose_name=_('Activity Time To'))
    reservation_time = models.DateTimeField(
        verbose_name=_('Reservation Time'), auto_now_add=True)
    comment = models.TextField(verbose_name=_('Comment'))

    class Meta:
        verbose_name = _('Site Reservation')
        verbose_name_plural = _('Site Reservation')
        default_permissions = ('add', 'delete', 'update', 'view')
