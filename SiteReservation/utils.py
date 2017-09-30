#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-21 18:19
# Last modified: 2017-09-25 09:32
# Filename: utils.py
# Description:
from typing import Iterable

from django.db.models import Q

from SiteReservation import RESERVATION_APPROVED
from SiteReservation.models import Reservation


def is_conflict(start, end, site, ignore=None):
    q = Reservation.objects.filter(status=RESERVATION_APPROVED)
    q = q.filter(Q(site=site))
    q = q.filter(Q(activity_time_to__gt=start) &
                 Q(activity_time_from__lt=end))
    if ignore is not None:
        if isinstance(ignore, Iterable):
            q = q.exclude(uid__in=ignore)
        else:
            q = q.exclude(uid=ignore)
    cnt = q.count()
    return cnt != 0
