# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 21:11
from __future__ import unicode_literals

from django.db import migrations


EMAIL_TEMPLATE = "{}@igw.tuwien.ac.at"

def set_tuwel_stream_ids(apps, schema_editor):
    Course = apps.get_model("Course", "Course")
    for course in Course.objects.all():
        if course.tuwel_course_stream_id is not None:
            continue
        if course.short_title == "hci":
            course.tuwel_course_stream_id = 363079
        elif course.short_title == "gsi":
            course.tuwel_course_stream_id = 363094
        else:
            course.tuwel_course_stream_id = 0
        course.save()


def set_emails(apps, schema_editor):
    Course = apps.get_model("Course", "Course")
    for course in Course.objects.all():
        if course.email is not None:
            continue
        if course.short_title == "hci":
            course.email = EMAIL_TEMPLATE.format("bhci")
            # default case works for gsi
        else:
            course.email = EMAIL_TEMPLATE.format(course.short_title)
        course.save()


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0012_auto_20171016_2110'),
    ]

    operations = [
        migrations.RunPython(set_tuwel_stream_ids, lambda a, s: None),
        migrations.RunPython(set_emails, lambda a, s: None),
    ]