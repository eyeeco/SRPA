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
    url(r'^detail/(?P<uid>.+)$', views.ProjectDetail.as_view(), name='detail'),
    url(r'^add/$', views.ProjectAdd.as_view(), name='add'),
    url(r'^update/(?P<uid>.+)$', views.ProjectUpdate.as_view(),
        name='update'),
    url(r'^social_add/(?P<uid>.+)$', views.ProjectSocialAdd.as_view(),
        name='social_add'),
    url(r'^export/(?P<uid>.+)$', views.ProjectExport.as_view(),
        name='export'),
    url(r'^cancel/(?P<uid>.+)$', views.ProjectCancel.as_view(),
        name='cancel'),
    url(r'^project_end/(?P<uid>.+)$', views.ProjectEnd.as_view(),
        name='project_end'),
]

admin_patterns = [
    url(r'^list/(?P<page>\d+)$', views.AdminProjectList.as_view(),
        name='list'),
    url(r'^detail/(?P<uid>.+)$', views.AdminProjectDetail.as_view(),
        name='detail'),
    url(r'^update/(?P<uid>.+)$', views.AdminProjectUpdate.as_view(),
        name='update'),
    url(r'^update_plus/(?P<uid>.+)$', views.AdminProjectUpdatePlus.as_view(),
        name='update_plus'),
]


urlpatterns = [
    url(r'^$', views.ProjectIndex.as_view(), name='index'),
    url(r'^ordinary/', include(ord_patterns, namespace='ordinary')),
    url(r'^admin/', include(admin_patterns, namespace='admin')),
]
