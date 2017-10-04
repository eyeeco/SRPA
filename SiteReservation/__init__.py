#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-07 19:24
# Last modified: 2017-10-04 16:10
# Filename: __init__.py
# Description:
from django.utils.translation import ugettext_lazy as _


RESERVATION_SUBMITTED = 0
RESERVATION_CANCELLED = 1
RESERVATION_APPROVED = 2
RESERVATION_EDITTING = 3
RESERVATION_TERMINATED = 4
RESERVATION_STATUS = (
    (RESERVATION_SUBMITTED, _('Reservation Submitted')),
    (RESERVATION_CANCELLED, _('Reservation Cancelled')),
    (RESERVATION_APPROVED, _('Reservation Approved')),
    (RESERVATION_EDITTING, _('Reservation Editting')),
    (RESERVATION_TERMINATED, _('Reservation Terminated')),
)

RESERVATION_STATUS_CAN_EDIT = (
    RESERVATION_SUBMITTED, RESERVATION_EDITTING)

RESERVATION_STATUS_CAN_CHECK = (
    RESERVATION_SUBMITTED, RESERVATION_APPROVED,
    RESERVATION_EDITTING)

RESERVATION_STATUS_CAN_CANCEL = (
    RESERVATION_SUBMITTED, RESERVATION_EDITTING)
