# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-14 01:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectApproval', '0010_auto_20171009_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budget',
            options={'default_permissions': ('add', 'delete', 'update', 'view'), 'ordering': ['id'], 'verbose_name': 'Budget', 'verbose_name_plural': 'Budget'},
        ),
    ]
