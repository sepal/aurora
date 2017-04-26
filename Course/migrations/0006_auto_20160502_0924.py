# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0005_auto_20160429_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseuserrelation',
            name='review_karma',
            field=models.DecimalField(decimal_places=19, default=0.0, max_digits=20),
        ),
    ]
