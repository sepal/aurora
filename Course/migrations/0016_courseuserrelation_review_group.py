# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0015_auto_20171031_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuserrelation',
            name='review_group',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
