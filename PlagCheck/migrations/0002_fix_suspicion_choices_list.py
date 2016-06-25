# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='suspicion',
            options={'ordering': ['created']},
        ),
        migrations.AlterField(
            model_name='suspicion',
            name='state',
            field=models.CharField(choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED'), (4, 'SUSPECTED_SELF_PLAGIARISM')], max_length=2, default=0),
        ),
    ]
