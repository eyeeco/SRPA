#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:16
# Last modified: 2017-09-09 09:39
# Filename: urls.py
# Description:
from django.conf.urls import url, include

from . import views


ord_patterns = [
    url(r'^list/(?P<page>\d+)$', views.ProjectList.as_view(), name='list'),
    url(r'^detail/$', views.ProjectDetail.as_view(), name='detail'),
    url(r'^add/$', views.ProjectAdd.as_view(), name='add'),
    url(r'^update/$', views.ProjectUpdate.as_view(),
        name='update'),
]

admin_patterns = [
    url(r'^list/$', views.AdminProjectList.as_view(), name='list'),
    url(r'^detail/$', views.AdminProjectDetail.as_view(), name='detail'),
    url(r'^update/$', views.AdminProjectUpdate.as_view(),
        name='update'),
]


urlpatterns = [
    url(r'^$', views.ProjectIndex.as_view(), name='index'),
    url(r'^ordinary/', include(ord_patterns, namespace='ordinary')),
    url(r'^admin/', include(admin_patterns, namespace='admin')),
]
