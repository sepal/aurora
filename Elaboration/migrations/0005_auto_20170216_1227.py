# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Elaboration', '0004_elaboration_most_helpful_other_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='elaboration',
            name='extra_review_question',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
