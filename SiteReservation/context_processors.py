#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-16 10:55
# Last modified: 2017-09-18 15:00
# Filename: context_processors.py
# Description:
from SiteReservation import RESERVATION_SUBMITTED, RESERVATION_CANCELLED
from SiteReservation import RESERVATION_APPROVED, RESERVATION_EDITTING
from SiteReservation import RESERVATION_TERMINATED, RESERVATION_CONFIRMED
from SiteReservation import RESERVATION_FINISHED
from SiteReservation import RESERVATION_STATUS_STUDENT


def expose_consts(request):
    consts = {
            'RESERVATION_SUBMITTED': RESERVATION_SUBMITTED,
            'RESERVATION_CANCELLED': RESERVATION_CANCELLED,
            'RESERVATION_APPROVED': RESERVATION_APPROVED,
            'RESERVATION_TERMINATED': RESERVATION_TERMINATED,
            'RESERVATION_CONFIRMED': RESERVATION_CONFIRMED,
            'RESERVATION_FINISHED': RESERVATION_FINISHED,
            'RESERVATION_STATUS_STUDENT_ACTIONS': RESERVATION_STATUS_STUDENT,
    }
    return consts
