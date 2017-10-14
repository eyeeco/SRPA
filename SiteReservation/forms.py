#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-14 14:39
# Last modified: 2017-10-14 09:57
# Filename: forms.py
# Description:
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta, timezone

from const.models import CaptchaField, Site
from SiteReservation.models import Reservation
from SiteReservation import RESERVATION_APPROVED
from django.db.models import Q


class DateForm(forms.Form):
    date = forms.DateField(
        label=_('Date'),
        widget=forms.TextInput(attrs={
            'readonly': 'true',
            'class': 'form-control'}))
    site = forms.ModelChoiceField(
        label=_('Site'),
        queryset=Site.objects.all().order_by('desc'),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }))

    def clean(self):
        cleaned_data = super(DateForm, self).clean()
        errors = {}
        t = cleaned_data.get('date')

        if t is not None and t < datetime.now().date():
            errors['date'] = [_('Please choose a future time')]

        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class ReservationForm(ModelForm):
    activity_time_from = forms.DateTimeField(
        label=_('Activity Time From'),
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:00:00'))
    activity_time_to = forms.DateTimeField(
        label=_('Activity Time To'),
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:00:00'))

    class Meta:
        model = Reservation
        fields = ['site', 'workshop', 'title',
                  'activity_time_from', 'activity_time_to', 'comment']

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        errors = {}
        t1 = cleaned_data.get('activity_time_from')
        t2 = cleaned_data.get('activity_time_to')

        if t1.hour < 8 or t1.hour > 22:
            errors['activity_time_from'] = [
                _('Activity time should between 8 am and 10 pm')]

        if t2.hour < 8 or t2.hour > 22:
            errors['activity_time_to'] = [
                _('Activity time should between 8 am and 10 pm')]

        if t2 <= t1:
            if 'activity_time_to' in errors:
                errors['activity_time_to'].append(
                    _('Activity Time To should be '
                      'later than Activity Time From'))
            else:
                errors['activity_time_to'] = [
                    _('Activity Time To should be '
                      'later than Activity Time From')]

        if (t2 - t1).total_seconds() / 3600 > 4:
            if 'activity_time_to' in errors:
                errors['activity_time_to'].append(
                    _('Reservation can not be '
                      'longer than 4 hours'))
            else:
                errors['activity_time_to'] = [
                    _('Reservation can not be '
                      'longer than 4 hours')]

        if t1 < datetime.now(timezone.utc) + timedelta(days=2):
            if 'activity_time_from' in errors:
                errors['activity_time_from'].append(
                    _('Can only reserve later than two days after now'))
            else:
                errors['activity_time_from'] = [
                    _('Can only reserve later than two days after now')]

        if t1.date() != t2.date():
            if 'activity_time_to' in errors:
                errors['activity_time_to'].append(
                    _('Can only reserve within a day'))
            else:
                errors['activity_time_to'] = [
                    _('Can only reserve within a day')]

        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data
