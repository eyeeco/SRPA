#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:08
# Last modified: 2017-09-24 16:00
# Filename: urls.py
# Description:
"""SRPA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from authentication import views

urlpatterns = [
    url('^$', views.IndexView.as_view(), name='index'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^user/', include('authentication.urls', namespace='auth')),
    url(r'^reservation/', include('SiteReservation.urls',
        namespace='reservation')),
    url(r'^project/', include('ProjectApproval.urls',
        namespace='project')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
