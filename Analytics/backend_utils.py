#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-08 08:35
# Last modified: 2017-10-08 13:56
# Filename: backend_utils.py
# Description:
from .models import BehaviorFlow


def record_to_mysql(*args, **kwargs):
    BehaviorFlow.objects.create(**kwargs)


def record_to_redis(*args, **kwargs):
    pass
