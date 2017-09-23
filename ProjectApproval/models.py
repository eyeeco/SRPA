#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 19:33
# Last modified: 2017-09-20 20:11
# Filename: models.py
# Description:
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

from const.models import Workshop
from authentication.models import TeacherInfo
from . import PROJECT_STATUS, PROJECT_SUBMITTED
from . import ACTIVITY_RANGES, ACTIVITY_RANGE_WORKSHOP
from .utils import get_user_project_attachments_path


class Project(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, verbose_name='申请人',
                             on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, verbose_name='工坊',
                                 on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='状态',
                                 choices=PROJECT_STATUS,
                                 default=PROJECT_SUBMITTED)
    title = models.CharField(verbose_name='活动名称', max_length=100)
    apply_time = models.DateTimeField(verbose_name='申请时间',
                                      auto_now_add=True)
    activity_time_from = models.DateTimeField(verbose_name='活动开始时间')
    activity_time_to = models.DateTimeField(verbose_name='活动结束时间')
    site = models.CharField(verbose_name='活动场地', max_length=100)
    form = models.CharField(verbose_name='活动形式', max_length=30)
    charger = models.CharField(verbose_name='活动负责人', max_length=20)
    contact_info = models.CharField(verbose_name='联系方式', max_length=30)
    activity_range = models.IntegerField(verbose_name='活动范围',
                                         choices=ACTIVITY_RANGES,
                                         default=ACTIVITY_RANGE_WORKSHOP)
    amount = models.IntegerField(verbose_name='参与人数')
    has_social = models.BooleanField(verbose_name='是否有校外人员参与')
    budget = models.TextField(verbose_name='活动预算及说明')
    comment = models.TextField(verbose_name='备注')
    content = models.TextField(verbose_name='活动内容', default='')
    instructor_comment = models.TextField(verbose_name='指导教师意见',
                                          blank=True)
    attachment = models.FileField(
        verbose_name='上传附件', blank=True,
        upload_to=get_user_project_attachments_path)

    class Meta:
        verbose_name = '活动项目'
        verbose_name_plural = '活动项目'
        default_permissions = ('add', 'delete', 'update', 'view')


class SocialInvitation(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False, unique=True)
    project = models.ForeignKey(Project, verbose_name='活动项目',
                                on_delete=models.CASCADE)
    socials_info = models.TextField(verbose_name='校外人员名单')
    attend_info = models.TextField(verbose_name='校外人员参与活动情况说明')
    ideology_info = models.TextField(
        verbose_name='校外人员思想意识形态情况说明')

    class Meta:
        verbose_name = '邀请校外人员申请表'
        verbose_name_plural = '邀请校外人员申请表'
        default_permissions = ('add', 'delete', 'update', 'view')
