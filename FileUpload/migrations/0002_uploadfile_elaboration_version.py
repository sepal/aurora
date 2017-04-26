# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FileUpload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='elaboration_version',
            field=models.TextField(default='original'),
            preserve_default=True,
        ),
    ]
