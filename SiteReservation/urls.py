#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 08:48
# Last modified: 2017-09-22 09:44
# Filename: urls.py
# Description:
from django.conf.urls import url, include

from . import views


ord_patterns = [
    url(r'^list/(?P<page>\d+)$', views.ReservationList.as_view(), name='list'),
    url(r'^detail/(?P<uid>.+)$', views.ReservationDetail.as_view(),
        name='detail'),
    url(r'^add/$', views.ReservationAdd.as_view(), name='add'),
    url(r'^update/(?P<uid>.+)$', views.ReservationUpdate.as_view(),
        name='update'),
    url(r'^terminate/(?P<uid>.+)$', views.ReservationTerminate.as_view(),
        name='terminate'),
    url(r'^export/(?P<uid>.+)$', views.ReservationExport.as_view(),
        name='export'),
]

admin_patterns = [
    url(r'^list/(?P<page>\d+)$', views.AdminReservationList.as_view(),
        name='list'),
    url(r'^detail/(?P<uid>.+)$', views.AdminReservationDetail.as_view(),
        name='detail'),
    url(r'^update/(?P<uid>.+)$', views.AdminReservationUpdate.as_view(),
        name='update'),
]


urlpatterns = [
    url(r'^$', views.ReservationIndex.as_view(), name='index'),
    url(r'^status/', views.ReservationStatus.as_view(), name='status'),
    url(r'^ordinary/', include(ord_patterns, namespace='ordinary')),
    url(r'^admin/', include(admin_patterns, namespace='admin')),
]
