# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-22 01:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('const', '0004_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='审阅时间'),
            preserve_default=False,
        ),
    ]