# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0004_rename_suspect_into_suspicion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reference',
            old_name='stored_doc',
            new_name='suspect_doc',
        ),
        migrations.RenameField(
            model_name='result',
            old_name='stored_doc',
            new_name='doc',
        ),
        migrations.RenameField(
            model_name='suspicion',
            old_name='stored_doc',
            new_name='suspect_doc',
        ),
        migrations.RenameField(
            model_name='suspicion',
            old_name='similar_to',
            new_name='similar_doc',
        ),
    ]
