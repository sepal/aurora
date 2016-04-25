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
            name='review_karma',
            field=models.DecimalField(decimal_places=2, max_digits=5, default=50.0),
            preserve_default=True,
        ),
    ]
