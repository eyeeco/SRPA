#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:03
# Last modified: 2017-10-04 15:11
# Filename: admin.py
# Description:
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DetailView
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Q
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin

from .ordinary import ReservationList, ReservationUpdate, ReservationDetail

from const.forms import FeedBackForm
from const.models import FeedBack
from SiteReservation import RESERVATION_STATUS_CAN_CHECK, RESERVATION_EDITTING
from SiteReservation import RESERVATION_APPROVED, RESERVATION_TERMINATED
from SiteReservation import RESERVATION_CANCELLED
from SiteReservation.models import Reservation
from SiteReservation.utils import is_conflict
from authentication.models import UserInfo, StudentInfo


#  TODO: LoginRequiredMixin --> PermissionRequiredMixin
class AdminReservationBase(LoginRequiredMixin):
    """
    A base view for all admin reservation actions. SHOULD NOT DIRECTLY USE
    THIS. Check admin auth first.
    """

    model = Reservation


class AdminReservationList(AdminReservationBase, PermissionListMixin, 
                           ListView):
    """
    A view for displaying reservations list for admin. GET only.
    """
    paginate_by = 12
    permission_required = 'view_reservation'
    ordering = ['status', '-reservation_time']
    template = 'SiteReservation/reservation_list.html'

    def get_queryset(self):
        groups = self.request.user.groups.all()
        queryset = super().get_queryset().filter(workshop__group=groups)
        return queryset.filter(~Q(status=RESERVATION_CANCELLED))


class AdminReservationDetail(AdminReservationBase, PermissionRequiredMixin, 
                             DetailView):
    """
    A view for displaying specified reservation for admin. GET only.
    """
    raise_exception = True
    permission_required = 'view_reservation'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        form = FeedBackForm({'target_uid': self.object.uid})
        kwargs['form'] = form
        feedbacks = FeedBack.objects.filter(target_uid=self.object.uid)
        feedbacks.order_by('-created')
        kwargs['feedbacks'] = feedbacks
        student = Reservation.objects.get(uid=self.object.uid)
        student_info = StudentInfo.objects.get(user_info__user=student.user)
        kwargs['student_info'] = student_info
        return super(AdminReservationDetail, self).get_context_data(**kwargs)


class AdminReservationUpdate(AdminReservationBase, PermissionRequiredMixin, 
                             UpdateView):
    """
    A view for admin to update an exist reservation.
    Should check status before change, reject change if not match
    specified status.
    """
    raise_exception = True
    permission_required = 'update_reservation'
    http_method_names = ['post']
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = FeedBackForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        allowed_status = self.object.status in RESERVATION_STATUS_CAN_CHECK
        if not allowed_status:
            return HttpResponseForbidden()
        return super(AdminReservationUpdate, self).post(request, *args,
                                                        **kwargs)

    def get_form_kwargs(self):
        return {'data': self.request.POST}

    def form_valid(self, form):
        obj = self.object
        feedback = form.save(commit=False)
        if obj.uid != feedback.target_uid:
            # Mismatch target_uid
            return JsonResponse({'status': 2, 'reason': _('Illegal Input')})
        feedback.user = self.request.user
        status = form.cleaned_data['status']
        if status == 'APPROVE':
            conflict = is_conflict(obj.activity_time_from,
                                   obj.activity_time_to,
                                   obj.site)
            if conflict:
                return JsonResponse({'status': 3,
                                     'reason': _('Conflict with existing '
                                                 'reservation')})
            obj.status = RESERVATION_APPROVED
        elif status == 'EDITTING':
            obj.status = RESERVATION_EDITTING
        elif status == 'TERMINATED':
            obj.status = RESERVATION_TERMINATED
        obj.save()
        feedback.save()
        return JsonResponse({'status': 0})

    def form_invalid(self, form):
        return JsonResponse({'status': 1, 'reason': _('Illegal Input')})
