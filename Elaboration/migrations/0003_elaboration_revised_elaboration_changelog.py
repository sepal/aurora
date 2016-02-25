# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Elaboration', '0002_elaboration_revised_elaboration_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='elaboration',
            name='revised_elaboration_changelog',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
