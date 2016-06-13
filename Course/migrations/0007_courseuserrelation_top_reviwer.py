# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0006_auto_20160502_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuserrelation',
            name='top_reviewer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
