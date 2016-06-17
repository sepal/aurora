# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0005_rename_stored_doc_into_suspect_doc_and_similar_to_into_similar'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Store',
            new_name='Document',
        ),
        migrations.AlterField(
            model_name='suspicion',
            name='similar_doc',
            field=models.ForeignKey(related_name='suspicion_similar', to='PlagCheck.Document'),
        ),
    ]
