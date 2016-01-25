# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
