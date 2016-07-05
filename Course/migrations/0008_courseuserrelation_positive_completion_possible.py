# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0007_courseuserrelation_top_reviwer'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuserrelation',
            name='positive_completion_possible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
