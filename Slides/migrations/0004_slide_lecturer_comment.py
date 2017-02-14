# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Slides', '0003_auto_20170131_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='lecturer_comment',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
