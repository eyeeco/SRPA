#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-09 09:49
# Last modified: 2017-09-24 10:01
# Filename: utils.py
# Description:
import os.path as osp

from uuid import uuid4
from datetime import datetime

from django.conf import settings
from xlwt import Workbook, easyxf, Alignment, Borders


def get_user_project_attachments_path(instance, filename):
    now = datetime.now()
    return 'project_attachments/{}/{:04d}/{:02d}/{:02d}/{}'.format(
        instance.user.id, now.year, now.month, now.day, filename)


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


def export_project(project, max_budget_row=5):
    book = Workbook(encoding='utf-8')
    sheet = book.add_sheet('sheet1')
    sheet.footer_str = b''
    sheet.header_str = 'ID:{}'.format(project.uid).encode()
    sheet.write_merge(0, 0, 0, 11, '大连理工大学创意工社活动申请表',
                      style=title_style)
    sheet.write_merge(1, 1, 0, 1, '工社名称', style=header_style)
    sheet.write_merge(1, 1, 2, 5, str(project.workshop), style=header_style)
    sheet.write_merge(1, 1, 6, 7, '活动名称', style=header_style)
    sheet.write_merge(1, 1, 8, 11, project.title, style=header_style)
    sheet.write_merge(2, 2, 0, 1, '活动地点', style=header_style)
    sheet.write_merge(2, 2, 2, 5, project.site, style=header_style)
    sheet.write_merge(2, 2, 6, 7, '活动时间', style=header_style)
    activity_time = '开始:{}\n结束:{}'.format(
        project.activity_time_from, project.activity_time_to)
    sheet.write_merge(2, 2, 8, 11, activity_time, style=header_style)
    sheet.write_merge(3, 3, 0, 1, '活动负责人', style=header_style)
    sheet.write_merge(3, 3, 2, 5, project.user.first_name, style=header_style)
    sheet.write_merge(3, 3, 6, 7, '联系方式', style=header_style)
    sheet.write_merge(3, 3, 8, 11, project.contact_info, style=header_style)
    sheet.write_merge(4, 5, 0, 1, '参与对象及人数', style=header_style)
    range_amount = '参与对象:{}\n人数:{}人'.format(
        project.activity_range, project.amount)
    sheet.write_merge(4, 5, 2, 11, range_amount, style=header_style)
    sheet.write_merge(6, 7, 0, 1, '是否有校外人员', style=header_style)
    sheet.write_merge(6, 7, 2, 11, '是' if project.has_social else '否',
                      style=header_style)
    sheet.write_merge(8, 11, 0, 0, '活动内容简介', style=header_style)
    sheet.write_merge(8, 11, 1, 11, project.content, style=content_style)
    sheet.write_merge(12, 13 + max_budget_row, 0, 0, '活动预算',
                      style=header_style)
    sheet.write_merge(12, 12, 1, 3, '预算', style=budget_style)
    sheet.write_merge(12, 12, 4, 7, '预算金额(元)', style=budget_style)
    sheet.write_merge(12, 12, 8, 11, '描述', style=budget_style)
    row_offset = 1
    budgets = [x.strip().split(' ') for x in project.budget.split('\n')]
    total_budget = sum(int(budget) for item, budget, desc in budgets)
    if len(budgets) > max_budget_row:
        rest_budget = sum(int(budget) for item, budget, desc
                          in budgets[max_budget_row:])
        budgets[max_budget_row:] = [['其他', rest_budget, '无']]
    else:
        budgets.extend(['', '', ''] for _ in
                       range(max_budget_row - len(budgets)))
    for item, budget, desc in budgets:
        sheet.write_merge(12 + row_offset, 12 + row_offset, 1, 3, item,
                          style=budget_style)
        sheet.write_merge(12 + row_offset, 12 + row_offset, 4, 7, budget,
                          style=budget_style)
        sheet.write_merge(12 + row_offset, 12 + row_offset, 8, 11, desc,
                          style=budget_style)
        row_offset += 1
    sheet.write_merge(13 + max_budget_row, 13 + max_budget_row, 1, 3, '合计',
                      style=budget_style)
    sheet.write_merge(13 + max_budget_row, 13 + max_budget_row, 4, 7,
                      total_budget, style=budget_style)
    sheet.write_merge(13 + max_budget_row, 13 + max_budget_row, 8, 11, '',
                      style=budget_style)
    sheet.write_merge(14 + max_budget_row, 14 + max_budget_row, 0, 2,
                      '活动负责人签字', style=header_style)
    sheet.write_merge(14 + max_budget_row, 14 + max_budget_row, 3, 7,
                      '指导教师签字', style=header_style)
    sheet.write_merge(14 + max_budget_row, 14 + max_budget_row, 8, 11,
                      '学院意见', style=header_style)
    sheet.write_merge(15 + max_budget_row, 16 + max_budget_row, 0, 2,
                      '日期:', style=signature_style)
    sheet.write_merge(15 + max_budget_row, 16 + max_budget_row, 3, 7,
                      '日期:', style=signature_style)
    sheet.write_merge(15 + max_budget_row, 16 + max_budget_row, 8, 11,
                      '日期:', style=signature_style)

    for col in range(0, 12):
        sheet.col(col).width = 256 * 7
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = 1400
    for row in range(1, 15 + max_budget_row):
        sheet.row(row).height_mismatch = True
        sheet.row(row).height = 600
    sheet.row(15 + max_budget_row).height_mismatch = True
    sheet.row(15 + max_budget_row).height = 1200

    fname = '{}.xls'.format(project.uid)
    save_path = osp.join(settings.TMP_FILES_ROOT, fname)
    book.save(save_path)
    url_path = osp.join(settings.TMP_FILES_URL, fname)
    return url_path
