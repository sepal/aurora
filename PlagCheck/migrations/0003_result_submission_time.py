# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0002_remove_filter_rename_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='submission_time',
            field=models.DateTimeField(default=datetime.date(2016, 6, 16)),
            preserve_default=False,
        ),
    ]
