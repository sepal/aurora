# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suspectfilter',
            name='stored_doc',
        ),
        migrations.DeleteModel(
            name='SuspectFilter',
        ),
        migrations.AlterModelOptions(
            name='suspect',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='store',
            old_name='doc_id',
            new_name='elaboration_id',
        ),
        migrations.AlterField(
            model_name='store',
            name='is_revised',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='suspect',
            name='state',
            field=models.CharField(max_length=2, choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED')], default=0),
        ),
    ]
