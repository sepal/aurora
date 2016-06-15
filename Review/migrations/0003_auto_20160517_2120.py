# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0002_review_chosen_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='chosen_by',
            field=models.CharField(default='random', max_length=100, null=True, blank=True),
        ),
    ]
