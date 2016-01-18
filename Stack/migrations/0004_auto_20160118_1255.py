# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Stack', '0003_auto_20160106_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stack',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
        migrations.AlterField(
            model_name='stack',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
