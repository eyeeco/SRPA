#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-07 21:05
# Last modified: 2017-10-08 13:56
# Filename: settings.py
# Description:
from django.conf import settings


IGNORE_ANONYMOUS = getattr(settings, 'TRACK_ANONYMOUS', False)

IGNORE_METHODS = getattr(settings, 'TRACK_METHODS', ())

IGNORE_STATUSES = getattr(settings, 'IGNORE_STATUSES', ())

IGNORE_PREFIXES = getattr(settings, 'IGNORE_PREFIXES', ())

IGNORE_IPS = getattr(settings, 'IGNORE_IPS', ())

IP_HEADERS = getattr(settings, 'IP_HEADERS',
                     ('HTTP_X_REAL_IP', 'HTTP_CLIENT_IP',
                      'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'))

DB_BACKENDS = getattr(settings, 'DB_BACKENDS', ('mysql'))

assert DB_BACKENDS
