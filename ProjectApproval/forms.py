from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from ProjectApproval.models import Project


class AddActivityForm(ModelForm):

    budget = forms.CharField(
        label='预算及说明',
        widget=forms.Textarea(attrs={"rows": 3}))
    comment = forms.CharField(
        label='备注',
        widget=forms.Textarea(attrs={"rows": 3}))
    activity_time_from = forms.CharField(
        label='活动开始时间',
        widget=forms.DateTimeInput(
            attrs={'class': 'datetimepicker form-control'}),
        required=False)
    activity_time_to = forms.CharField(
        label='活动结束时间',
        widget=forms.DateTimeInput(
            attrs={'class': 'datetimepicker form-control'}),
        required=False)

    class Meta:
        model = Project
        fields = ['title', 'workshop', 'activity_time_from',
                  'activity_time_to', 'site', 'form', 'charger',
                  'contact_info', 'activity_range', 'amount', 'has_social',
                  'budget', 'comment', 'instructor_comment',
                  'attachment']
