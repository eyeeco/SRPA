#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-08 20:15
# Last modified: 2017-10-14 10:18
# Filename: __init__.py
# Description:
from .auth import IndexView, LoginView, CaptchaRefresh
from .auth import StudentRegisterView
from .info_detail import StudentInfoDetail
from .info_update import StudentInfoUpdate
from .admin import AdminIndex, AdminWorkshopAdd, AdminWorkshopUpdate
from .admin import AdminWorkshopDetail, AdminTeacherAdd
from .admin import AdminTeacherUpdate, AdminTeacherDetail
from .admin import AdminTeacherList, AdminWorkshopList
from .admin import AdminSiteAdd, AdminSiteUpdate, AdminSiteDetail
from .admin import AdminSiteList

__all__ = [
    'IndexView', 'LoginView', 'CaptchaRefresh',
    'StudentRegisterView',
    'StudentInfoDetail', 'SocialInfoDetail',
    'StudentInfoUpdate', 'SocialInfoUpdate',
    'AdminIndex', 'AdminWorkshopAdd',
    'AdminWorkshopUpdate', 'AdminWorkshopDetail',
    'AdminTeacherAdd', 'AdminTeacherUpdate',
    'AdminTeacherDetail', 'AdminTeacherList',
    'AdminWorkshopList', 'AdminSiteAdd',
    'AdminSiteUpdate', 'AdminSiteDetail',
    'AdminSiteList',
]
