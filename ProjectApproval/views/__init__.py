#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:20
# Last modified: 2017-09-09 09:39
# Filename: __init__.py
# Description:
from .ordinary import ProjectList, ProjectAdd, ProjectUpdate, ProjectIndex
from .ordinary import ProjectDetail, ProjectSocialAdd
from .admin import AdminProjectList, AdminProjectUpdate, AdminProjectDetail


__all__ = [
    'ProjectDetail', 'AdminProjectDetail',
    'ProjectList', 'ProjectAdd', 'ProjectUpdate',
    'AdminProjectList', 'AdminProjectUpdate',
    'ProjectSocialAdd'
]
