# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0004_courseuserrelation_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseuserrelation',
            name='review_group',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courseuserrelation',
            name='review_karma',
            field=models.DecimalField(max_digits=10, decimal_places=8, default=0.0),
            preserve_default=True,
        ),
    ]
