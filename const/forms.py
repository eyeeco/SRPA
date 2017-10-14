#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-21 16:23
# Last modified: 2017-10-14 10:33
# Filename: forms.py
# Description:
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from const.models import FeedBack


class FeedBackForm(ModelForm):
    target_uid = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'class': 'form-control'}))
    status = forms.ChoiceField(choices=(
        ('APPROVE', _('Feedback Approve')),
        ('EDITTING', _('Feedback Editting')),
        ('TERMINATED', _('Feedback teminated'))),
        widget=forms.Select(attrs={
            'class': 'form-control'}))
    desc = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('(Optional)Feedback Description')}))

    class Meta:
        model = FeedBack
        fields = ['target_uid', 'desc', 'status']
