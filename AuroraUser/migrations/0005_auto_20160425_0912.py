# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0004_aurorauser_review_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aurorauser',
            name='review_group',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
