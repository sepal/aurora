# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0008_courseuserrelation_positive_completion_possible'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tuwel_course_id',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
    ]
