# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 18:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stack', '0006_remove_stack_challenges'),
    ]

    operations = [
        migrations.AddField(
            model_name='stack',
            name='final_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
