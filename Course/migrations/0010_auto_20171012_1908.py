# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 19:08
from __future__ import unicode_literals

from django.db import migrations

def set_tuwel_ids(apps, schema_editor):
    Course = apps.get_model("Course", "Course")
    for course in Course.objects.all():
        if course.tuwel_course_id is not None:
            continue
        if course.short_title == "hci":
            course.tuwel_course_id = 5581
        elif course.short_title == "gsi":
            course.tuwel_course_id = 5575
        else:
            course.tuwel_course_id = 0
        course.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0009_course_tuwel_course_id'),
    ]

    operations = [
        migrations.RunPython(set_tuwel_ids, lambda a, s: None),
    ]
