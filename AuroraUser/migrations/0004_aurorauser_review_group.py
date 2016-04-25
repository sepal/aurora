# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0003_aurorauser_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='aurorauser',
            name='review_group',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
