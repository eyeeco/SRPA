# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-23 06:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectApproval', '0004_project_apply_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='content',
            field=models.TextField(default='', verbose_name='活动内容'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.IntegerField(choices=[(-1, '校外人员表单待填写'), (0, '申请已提交'), (1, '申请已取消'), (2, '活动进行中'), (3, '申请修改中'), (4, '活动已终止'), (5, '结项待审核'), (6, '结项修改中'), (7, '活动已完成'), (8, '活动已报销')], verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=100, verbose_name='标题'),
        ),
    ]
