from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from ProjectApproval.models import Project
from ProjectApproval.models import SocialInvitation


class ActivityForm(ModelForm):

    budget = forms.CharField(
        label='预算及说明',
        widget=forms.Textarea(attrs={"rows": 3}))
    comment = forms.CharField(
        label='备注',
        widget=forms.Textarea(attrs={"rows": 3}))
    content = forms.CharField(
        label='活动内容简介',
        widget=forms.Textarea(attrs={"rows": 3}))
    activity_time_from = forms.DateTimeField(
        label='活动开始时间',
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form_datetime_hour form-control'},
            format='%Y-%m-%d %H:00:00'),
        required=False)
    activity_time_to = forms.DateTimeField(
        label='活动结束时间',
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form_datetime_hour form-control'},
            format='%Y-%m-%d %H:00:00'),
        required=False)
    has_social = forms.CharField(
        label='是否有校外人员参与',
        widget=forms.CheckboxInput(attrs={}), required=False)

    class Meta:
        model = Project
        fields = ['title', 'workshop', 'activity_time_from',
                  'activity_time_to', 'site', 'form', 'charger',
                  'contact_info', 'activity_range', 'amount', 'has_social',
                  'budget', 'comment', 'instructor_comment',
                  'attachment', 'content']

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()
        errors = {}
        t1 = cleaned_data.get('activity_time_from')
        t2 = cleaned_data.get('activity_time_to')
        if t2 <= t1:
            if 'activity_time_to' in errors:
                errors['activity_time_to'].append('活动结束时间应晚于开始时间')
            else:
                errors['activity_time_to'] = ['活动结束时间应晚于开始时间']
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class SocialInvitationForm(ModelForm):

    socials_info = forms.CharField(
        label='校外人员名单',
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    attend_info = forms.CharField(
        label='校外人员参与活动情况说明',
        widget=forms.Textarea(attrs={
            'class': 'form-control social_info', 'rows': 3}))
    ideology_info = forms.CharField(
        label='校外人员思想意识形态情况说明',
        widget=forms.Textarea(attrs={
            'class': 'form-control social_info', 'rows': 3}))

    class Meta:
        model = SocialInvitation
        fields = ['socials_info', 'attend_info', 'ideology_info']
