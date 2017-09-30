#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-16 10:55
# Last modified: 2017-09-16 17:09
# Filename: context_processors.py
# Description:
from authentication import USER_IDENTITY_STUDENT, USER_IDENTITY_TEACHER
from authentication import USER_IDENTITY_ADMIN


def expose_consts(request):
    consts = {
        'USER_IDENTITY_STUDENT': USER_IDENTITY_STUDENT,
        'USER_IDENTITY_TEACHER': USER_IDENTITY_TEACHER,
        'USER_IDENTITY_ADMIN': USER_IDENTITY_ADMIN,
    }
    return consts
