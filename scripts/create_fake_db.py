#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-09-15 15:08
# Last modified: 2017-10-07 17:16
# Filename: create_fake_db.py
# Description:
import sys
import os
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SRPA.settings")
django.setup()

from django.contrib.auth.models import User, Group
from authentication import USER_IDENTITY_STUDENT, USER_IDENTITY_TEACHER
from authentication import INSTITUTES
from authentication.models import StudentInfo, TeacherInfo
from const.models import Site, Workshop
from SiteReservation.models import Reservation
from ProjectApproval.models import Project, SocialInvitation
from tools.utils import assign_perms


def create_student_info(num=10, prefix='student_'):
    students = []
    for i in range(1, 1 + num):
        user = User.objects.create_user(
            username=prefix + str(i),
            password=str(i),
            first_name=str(i))
        info = StudentInfo(
            user=user, identity=USER_IDENTITY_STUDENT,
            phone=str(i), student_id=str(i))
        info.save()
        assign_perms('studentinfo', user, info)
        assign_perms('reservation', user, perms='add',
                     app_name='SiteReservation')
        assign_perms('project', user, perms='add',
                     app_name='ProjectApproval')
        students.append(info)
    return students


def create_teacher_info(num=10, prefix='teacher_'):
    teachers = []
    for i in range(1, 1 + num):
        user = User.objects.create_user(
            username=prefix + str(i),
            password=str(i),
            first_name=str(i))
        info = TeacherInfo(
            user=user, identity=USER_IDENTITY_TEACHER)
        info.save()
        assign_perms('teacherinfo', user, info)
        teachers.append(info)
    return teachers


def create_site(num=10, prefix='site_'):
    for i in range(1, 1 + num):
        site = Site(desc=prefix + str(i))
        site.save()


def create_workshop(num=10, prefix='workshop_'):
    for i in range(1, 1 + num):
        desc = prefix + str(i)
        group, _ = Group.objects.get_or_create(name=desc)
        workshop = Workshop(desc=desc, group=group)
        workshop.save()


def main():
    create_student_info()
    teachers = create_teacher_info()
    create_site()
    create_workshop()


if __name__ == '__main__':
    main()
