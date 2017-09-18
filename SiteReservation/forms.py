#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-14 14:39
# Last modified: 2017-09-15 19:36
# Filename: forms.py
# Description:
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime, timedelta, timezone

from const.models import CaptchaField
from SiteReservation.models import Reservation
from SiteReservation import RESERVATION_APPROVED
from django.db.models import Q


class DateForm(forms.Form):
    date = forms.DateField(
        label='日期',
        widget=forms.TextInput(attrs={
            'readonly': 'true',
            'class': 'form-control'}))


class ReservationAddForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['site', 'workshop', 'title',
                  'activity_time_from', 'activity_time_to', 'comment']

    def clean(self):
        cleaned_data = super(ReservationAddForm, self).clean()
        errors = {}
        t1 = cleaned_data.get('activity_time_from')
        t2 = cleaned_data.get('activity_time_to')
        site_now = cleaned_data.get('site')

        if t1.hour < 8 or t1.hour > 22:
            errors['activity_time_from'] = ['活动应在早8点至晚10点间']

        if t2.hour < 8 or t2.hour > 22:
            errors['activity_time_to'] = ['活动时间应在早8点至晚10点间']

        if t2 <= t1:
            if 'activity_time_to' in errors:
                errors['activity_time_to'].append('活动结束时间应晚于开始时间')
            else:
                errors['activity_time_to'] = ['活动结束时间应晚于开始时间']

        if t1 < datetime.now(timezone.utc) + timedelta(days=2):
            if 'activity_time_from' in errors:
                errors['activity_time_from'].append('只能预约两天后的时间段')
            else:
                errors['activity_time_from'] = ['只能预约两天后的时间段']
        
        if t1.date() != t2.date():
            if 'activity_time_to' in errors:
                errors['activity_time_to'].append('只能预约同一天内的时间段')
            else:
                errors['activity_time_to'] = ['只能预约同一天内的时间段']

        q = Reservation.objects.filter(status=RESERVATION_APPROVED)
        q = q.filter(Q(site=site_now))
        b = q.filter(Q(activity_time_to__gt=t1) & Q(activity_time_from__lt=t2))
        qnum = b.count()
        if qnum != 0:
            errors['activity_time_to'] = ['该时间段内已存在预约']
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data
