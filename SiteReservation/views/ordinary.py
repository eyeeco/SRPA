#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:03
# Last modified: 2017-09-18 15:11
# Filename: ordinary.py
# Description:
from datetime import datetime, timedelta, timezone

from django.views.generic import ListView, CreateView, UpdateView, RedirectView
from django.views.generic import DetailView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse, NoReverseMatch
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from authentication import USER_IDENTITY_STUDENT, USER_IDENTITY_TEACHER
from authentication import USER_IDENTITY_ADMIN
from SiteReservation import RESERVATION_APPROVED
from SiteReservation.models import Reservation
from SiteReservation.forms import DateForm, ReservationAddForm
from const.models import Site
from tools.utils import assign_perms
from SiteReservation import RESERVATION_SUBMITTED, RESERVATION_STATUS_STUDENT


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class ReservationBase(LoginRequiredMixin):
    """
    A base view for all reservation actions. SHOULD NOT DIRECTLY USE THIS.
    """

    model = Reservation


class ReservationIndex(ReservationBase, TemplateView):
    template_name = 'SiteReservation/index.html'


class ReservationStatus(ReservationBase, FormView):
    template_name = 'SiteReservation/reservation_status.html'
    status_table_name = 'SiteReservation/status_table.html'
    form_class = DateForm

    def get_context_data(self, **kwargs):
        kwargs['sites'] = Site.objects.all().order_by('desc')
        return super(ReservationStatus, self).get_context_data(**kwargs)

    def form_valid(self, form):
        uid = self.request.POST.get('site_uid', None)
        date = form.cleaned_data['date']
        if date < datetime.now().date():
            return JsonResponse({'status': 2, 'reason': '请选择一个未来时间'})
        start_dt = datetime.combine(date, datetime.min.time())
        start_dt = start_dt.replace(tzinfo=timezone.utc)
        end_dt = start_dt + timedelta(days=1)
        if not uid:
            raise Http404()
        site = get_object_or_404(Site, uid=uid)
        reservations = Reservation.objects.filter(site=site)
        reservations = reservations.filter(status=RESERVATION_APPROVED)
        reservations = reservations.filter(
            activity_time_from__range=(start_dt, end_dt))  # day range
        available_status = [True for _ in range(14)]  # 0 -> 08:00 ~ 09:00
        for r in reservations:
            for hour in range(r.activity_time_from.hour,
                              r.activity_time_to.hour):
                available_status[hour] = False
        status_table = render_to_string(
            self.status_table_name, request=self.request,
            context={'available_status': available_status,
                     'date': date,
                     'site': site})
        return JsonResponse({'status': 0, 'html': status_table})

    def form_invalid(self, form):
        return JsonResponse({'status': 1, 'reason': '表单信息有误，请核对'})


class ReservationList(ReservationBase, ListView):
    """
    A view for displaying user-related reservations list. GET only.
    """

    def get_context_data(self, **kwargs):
        kwargs['RESERVATION_STATUS_STUDENT'] = RESERVATION_STATUS_STUDENT
        return super(ReservationList, self).get_context_data(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ReservationDetail(ReservationBase, DetailView):
    """
    A view for displaying specified reservation. GET only.
    """

    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class ReservationAdd(ReservationBase, CreateView):
    """
    A view for creating a new reservation.
    """
    template_name = 'SiteReservation/reservation_add.html'
    form_class = ReservationAddForm
    success_url = reverse_lazy('reservation:index')
    form_post_url = reverse_lazy('reservation:ordinary:add')

    def form_valid(self, form):
        site = form.cleaned_data['site']
        workshop = form.cleaned_data['workshop']
        title = form.cleaned_data['title']
        activity_time_from = form.cleaned_data['activity_time_from']
        activity_time_to = form.cleaned_data['activity_time_to']
        comment = form.cleaned_data['comment']

        reservation = Reservation.objects.create(
            user=self.request.user,
            site=site,
            workshop=workshop,
            status=RESERVATION_SUBMITTED,
            title=title,
            activity_time_from=activity_time_from,
            activity_time_to=activity_time_to,
            comment=comment)
        reservation.save()
        self.object = reservation
        assign_perms('reservation', self.request.user, obj=reservation)
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.success_url
        return super(ReservationAdd, self).get_context_data(**kwargs)


class ReservationUpdate(ReservationBase, UpdateView):
    """
    A view for updating an exist reservation. Should check status before
    change, reject change if not match specified status.
    """

    template_name = 'SiteReservation/reservation_update.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = ReservationAddForm
    success_url = reverse_lazy('reservation:index')
    form_post_url = 'reservation:ordinary:update'

    def get_context_data(self, **kwargs):
        kwargs['form_post_url'] = self.form_post_url
        kwargs['back_url'] = self.success_url
        return super(ReservationUpdate, self).get_context_data(**kwargs)

    def form_valid(self, form):
        return JsonResponse({'status': 0, 'redirect': self.success_url})

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        html = render_to_string(
            self.template_name, request=self.request,
            context=context)
        return JsonResponse({'status': 1, 'html': html})
