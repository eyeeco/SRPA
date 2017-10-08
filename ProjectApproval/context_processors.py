#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-10-04 16:09
# Last modified: 2017-10-04 16:17
# Filename: context_processors.py
# Description:
from ProjectApproval import PROJECT_SUBMITTED, PROJECT_CANCELLED
from ProjectApproval import PROJECT_APPROVED, PROJECT_EDITTING
from ProjectApproval import PROJECT_TERMINATED, PROJECT_END_SUBMITTED
from ProjectApproval import PROJECT_END_EDITTING, PROJECT_FINISHED
from ProjectApproval import PROJECT_COMPLETED
from ProjectApproval import PROJECT_STATUS_CAN_EDIT
from ProjectApproval import PROJECT_STATUS_CAN_CHECK
from ProjectApproval import PROJECT_STATUS_CAN_CANCEL
from ProjectApproval import PROJECT_STATUS_CAN_EXPORT
from ProjectApproval import PROJECT_STATUS_CAN_END_SUBMIT
from ProjectApproval import PROJECT_SOCIALFORM_REQUIRED
from ProjectApproval import PROJECT_STATUS_CAN_FINISH


def expose_consts(request):
    consts = {
        'PROJECT_SUBMITTED': PROJECT_SUBMITTED,
        'PROJECT_CANCELLED': PROJECT_CANCELLED,
        'PROJECT_APPROVED': PROJECT_APPROVED,
        'PROJECT_EDITTING': PROJECT_EDITTING,
        'PROJECT_TERMINATED': PROJECT_TERMINATED,
        'PROJECT_END_SUBMITTED': PROJECT_END_SUBMITTED,
        'PROJECT_END_EDITTING': PROJECT_END_EDITTING,
        'PROJECT_FINISHED': PROJECT_FINISHED,
        'PROJECT_COMPLETED': PROJECT_COMPLETED,
        'PROJECT_STATUS_CAN_EDIT': PROJECT_STATUS_CAN_EDIT,
        'PROJECT_STATUS_CAN_CANCEL': PROJECT_STATUS_CAN_CANCEL,
        'PROJECT_STATUS_CAN_CHECK': PROJECT_STATUS_CAN_CHECK,
        'PROJECT_SOCIALFORM_REQUIRED': PROJECT_SOCIALFORM_REQUIRED,
        'PROJECT_STATUS_CAN_EXPORT': PROJECT_STATUS_CAN_EXPORT,
        'PROJECT_STATUS_CAN_ENDED': PROJECT_STATUS_CAN_END_SUBMIT,
        'PROJECT_STATUS_CAN_FINISH': PROJECT_STATUS_CAN_FINISH
    }
    return consts
