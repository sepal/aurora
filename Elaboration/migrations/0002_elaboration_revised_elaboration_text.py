# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Elaboration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='elaboration',
            name='revised_elaboration_text',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
