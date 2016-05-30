# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0003_auto_20160215_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuserrelation',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
