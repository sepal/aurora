# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Elaboration', '0003_elaboration_revised_elaboration_changelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='elaboration',
            name='most_helpful_other_user',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
