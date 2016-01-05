# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Stack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stack',
            name='end_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stack',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
    ]
