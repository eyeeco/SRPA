#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-21 18:19
# Last modified: 2017-10-02 13:38
# Filename: utils.py
# Description:
import os.path as osp

from typing import Iterable

from django.db.models import Q
from django.conf import settings
from django.utils.timezone import get_current_timezone

from xlwt import Workbook, easyxf, Alignment, Borders

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


thick_border = easyxf('border: left thick, top thick, '
                      'bottom thick, right thick')

align_hc_vc = Alignment()
align_hc_vc.horz = Alignment.HORZ_CENTER
align_hc_vc.vert = Alignment.VERT_CENTER
align_hc_vc.wrap = True

align_hl_vt = Alignment()
align_hl_vt.horz = Alignment.HORZ_LEFT
align_hl_vt.vert = Alignment.VERT_TOP
align_hl_vt.wrap = True

align_hc_vb = Alignment()
align_hc_vb.horz = Alignment.HORZ_CENTER
align_hc_vb.vert = Alignment.VERT_BOTTOM
align_hc_vb.wrap = True

borders_thin = Borders()
borders_thin.left = Borders.THIN
borders_thin.right = Borders.THIN
borders_thin.bottom = Borders.THIN
borders_thin.top = Borders.THIN

borders_thick = Borders()
borders_thick.left = Borders.THICK
borders_thick.right = Borders.THICK
borders_thick.bottom = Borders.THICK
borders_thick.top = Borders.THICK

title_style = easyxf('font: name 黑体, bold on, height 360;')
title_style.alignment = align_hc_vc

header_style = easyxf('font: name 黑体, bold off, height 220;')
header_style.alignment = align_hc_vc
header_style.borders = borders_thin

content_style = easyxf('font: name 黑体, bold off, height 210;')
content_style.alignment = align_hl_vt
content_style.borders = borders_thin

value_style = easyxf('font: name 黑体, bold off, height 210;')
value_style.alignment = align_hc_vc
value_style.borders = borders_thin

budget_style = easyxf('font: name 黑体, bold off, height 210;')
budget_style.alignment = align_hc_vc
budget_style.borders = borders_thick

signature_style = easyxf('font: name 黑体, bold off, height 210;')
signature_style.alignment = align_hc_vb
signature_style.borders = borders_thin


def export_reservation(reservation):
    tz = get_current_timezone()
    book = Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheet1')
    sheet.footer_str = b''
    sheet.header_str = 'ID:{}'.format(reservation.uid).encode()
    sheet.write_merge(0, 0, 0, 11, '大连理工大学创意工社活动场地预约申请表',
                      style=title_style)
    sheet.write_merge(1, 1, 0, 1, '工社名称', style=header_style)
    sheet.write_merge(1, 1, 2, 5, str(reservation.workshop),
                      style=header_style)
    sheet.write_merge(1, 1, 6, 7, '活动名称', style=header_style)
    sheet.write_merge(1, 1, 8, 11, reservation.title, style=header_style)
    sheet.write_merge(2, 2, 0, 1, '活动场地', style=header_style)
    sheet.write_merge(2, 2, 2, 5, str(reservation.site),
                      style=header_style)
    sheet.write_merge(2, 2, 6, 7, '活动时间', style=header_style)
    time_from = reservation.activity_time_from.astimezone(tz)
    time_to = reservation.activity_time_to.astimezone(tz)
    activity_time = '开始:{}\n结束:{}'.format(
        time_from.strftime('%Y年%m月%d日 %H:%M'),
        time_to.strftime('%Y年%m月%d日 %H:%M'))
    sheet.write_merge(2, 2, 8, 11, activity_time, style=header_style)
    sheet.write_merge(3, 3, 0, 1, '活动负责人', style=header_style)
    sheet.write_merge(3, 3, 2, 5, reservation.user.first_name,
                      style=header_style)
    sheet.write_merge(3, 3, 6, 7, '预约时间', style=header_style)
    rtime = reservation.reservation_time.astimezone(tz)
    sheet.write_merge(3, 3, 8, 11, rtime.strftime('%Y年%m月%d日 %H:%M'),
                      style=header_style)
    sheet.write_merge(4, 8, 0, 0, '备注', style=header_style)
    sheet.write_merge(4, 8, 1, 11, reservation.comment, style=content_style)
    sheet.write_merge(9, 9, 0, 2,
                      '活动负责人签字', style=header_style)
    sheet.write_merge(9, 9, 3, 7,
                      '指导教师签字', style=header_style)
    sheet.write_merge(9, 9, 8, 11,
                      '学院意见', style=header_style)
    sheet.write_merge(10, 11, 0, 2,
                      '日期:', style=signature_style)
    sheet.write_merge(10, 11, 3, 7,
                      '日期:', style=signature_style)
    sheet.write_merge(10, 11, 8, 11,
                      '日期:', style=signature_style)

    for col in range(0, 12):
        sheet.col(col).width = 256 * 7
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = 1400
    for row in range(1, 11):
        sheet.row(row).height_mismatch = True
        sheet.row(row).height = 600
    sheet.row(15).height_mismatch = True
    sheet.row(15).height = 1200

    fname = '{}.xls'.format(reservation.uid)
    save_path = osp.join(settings.TMP_FILES_ROOT, fname)
    book.save(save_path)
    url_path = osp.join(settings.TMP_FILES_URL, fname)
    return url_path
