# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0002_auto_20151130_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='short_title',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
