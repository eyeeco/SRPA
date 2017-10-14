#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 09:10
# Last modified: 2017-10-14 10:21
# Filename: urls.py
# Description:
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views


info_update_patterns = [
    url(r'^student/(?P<uid>.+)$', views.StudentInfoUpdate.as_view(),
        name='student'),
]


info_patterns = [
    url(r'^student/(?P<uid>.+)$', views.StudentInfoDetail.as_view(),
        name='student'),
    url('^update/', include(info_update_patterns, namespace='update')),
]

register_patterns = [
    url(r'^$', views.StudentRegisterView.as_view(),
        name='index'),
]

admin_workshop_patterns = [
    url(r'^add/', views.AdminWorkshopAdd.as_view(), name='add'),
    url(r'^update/(?P<uid>.+)$', views.AdminWorkshopUpdate.as_view(),
        name='update'),
    url(r'^detail/(?P<uid>.+)$', views.AdminWorkshopDetail.as_view(),
        name='detail'),
    url(r'^list/(?P<page>\d+)$', views.AdminWorkshopList.as_view(),
        name='list'),
]

admin_site_patterns = [
    url(r'^add/', views.AdminSiteAdd.as_view(), name='add'),
    url(r'^update/(?P<uid>.+)$', views.AdminSiteUpdate.as_view(),
        name='update'),
    url(r'^detail/(?P<uid>.+)$', views.AdminSiteDetail.as_view(),
        name='detail'),
    url(r'^list/(?P<page>\d+)$', views.AdminSiteList.as_view(),
        name='list'),
]


admin_teacher_patterns = [
    url(r'^add/', views.AdminTeacherAdd.as_view(), name='add'),
    url(r'^update/(?P<uid>.+)$', views.AdminTeacherUpdate.as_view(),
        name='update'),
    url(r'^detail/(?P<uid>.+)$', views.AdminTeacherDetail.as_view(),
        name='detail'),
    url(r'^list/(?P<page>\d+)$', views.AdminTeacherList.as_view(),
        name='list'),
]

admin_patterns = [
    url(r'^$', views.AdminIndex.as_view(), name='index'),
    url(r'^workshop/', include(admin_workshop_patterns, namespace='workshop')),
    url(r'^site/', include(admin_site_patterns, namespace='site')),
    url(r'^teacher/', include(admin_teacher_patterns, namespace='teacher')),
]

urlpatterns = [
    url(r'^captcha/refresh/', views.CaptchaRefresh.as_view(),
        name='captcha_refresh'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(next_page='index'),
        name='logout'),
    url(r'^password_change/', auth_views.PasswordChangeView.as_view(
        template_name='authentication/password_change.html',
        success_url=reverse_lazy('auth:password_change_done')),
        name='password_change'),
    url(r'^password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
        name='password_change_done'),
    url(r'^register/', include(register_patterns, namespace='register')),
    url(r'^info/', include(info_patterns, namespace='info')),
    url(r'^admin/', include(admin_patterns, namespace='admin')),
]
