#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-07 20:58
# Last modified: 2017-10-08 13:56
# Filename: models.py
# Description:
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BehaviorFlow(models.Model):
    scheme = models.CharField(verbose_name=_('Scheme'), max_length=10)
    request_uri = models.CharField(verbose_name=_('URI'), max_length=256)
    request_method = models.CharField(verbose_name=_('Method'), max_length=10)
    request_referer = models.CharField(verbose_name=_('Referer'),
                                       max_length=256)
    request_user_agent = models.CharField(verbose_name=_('User-Agent'),
                                          max_length=256)
    request_user_id = models.CharField(verbose_name=_('User ID'),
                                       max_length=11)
    request_user_ip = models.GenericIPAddressField(verbose_name=_('IP'))
    response_status_code = models.CharField(verbose_name=_('Status Code'),
                                            max_length=3)
    response_render_time = models.FloatField(
        verbose_name=_('Response Render Time'))
    timestamp = models.DateTimeField(_('Timestamp'), default=timezone.now)

    class Meta:
        verbose_name = _('BehaviorFlow')
        verbose_name_plural = _('BehaviorFlow')
