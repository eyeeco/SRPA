#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 10:01
# Last modified: 2017-09-16 10:56
# Filename: context_processors.py
# Description:
from django.conf import settings as sys_settings


def expose_settings(request):
    settings = {
        'TITLE': sys_settings.TITLE,
    }
    return settings
