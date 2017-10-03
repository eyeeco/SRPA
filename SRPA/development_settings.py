#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-01 15:15
# Last modified: 2017-10-02 22:16
# Filename: development_settings.py
# Description:
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SRPA',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '192.168.3.95',
        'PORT': '3307',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        }
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
