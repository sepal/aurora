# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    replaces = [('PlagCheck', '0001_initial'), ('PlagCheck', '0002_remove_filter_rename_field'), ('PlagCheck', '0003_result_submission_time'), ('PlagCheck', '0004_rename_suspect_into_suspicion'), ('PlagCheck', '0005_rename_stored_doc_into_suspect_doc_and_similar_to_into_similar'), ('PlagCheck', '0006_rename_store_into_document')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('hash', models.CharField(db_index=True, max_length=255)),
            ],
            options=None,
            bases=None,
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hash_count', models.IntegerField()),
            ],
            options=None,
            bases=None,
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('doc_id', models.IntegerField()),
                ('text', models.TextField()),
                ('user_id', models.IntegerField(null=True)),
                ('user_name', models.CharField(max_length=100, null=True)),
                ('submission_time', models.DateTimeField(null=True)),
                ('is_revised', models.BooleanField()),
            ],
            options=None,
            bases=None,
        ),
        migrations.CreateModel(
            name='Suspect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('similarity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=2, default=0, choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'FILTER'), (4, 'AUTO_FILTERED'), (5, 'CITED')])),
                ('match_count', models.IntegerField()),
                ('result', models.ForeignKey(to='PlagCheck.Result')),
                ('similar_to', models.ForeignKey(to='PlagCheck.Store', related_name='suspected_similar_to')),
                ('stored_doc', models.ForeignKey(to='PlagCheck.Store', related_name='suspected_doc')),
            ],
            options=None,
            bases=None,
        ),
        migrations.AddField(
            model_name='result',
            name='stored_doc',
            field=models.ForeignKey(to='PlagCheck.Store'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reference',
            name='suspect_doc',
            field=models.ForeignKey(to='PlagCheck.Store'),
            preserve_default=True,
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
            field=models.CharField(max_length=2, default=0, choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED')]),
        ),
        migrations.AddField(
            model_name='result',
            name='submission_time',
            field=models.DateTimeField(default=datetime.date(2016, 6, 16)),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Suspicion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('similarity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=2, default=0, choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED')])),
                ('match_count', models.IntegerField()),
                ('result', models.ForeignKey(to='PlagCheck.Result')),
                ('similar_doc', models.ForeignKey(to='PlagCheck.Document', related_name='suspicion_similar')),
                ('suspect_doc', models.ForeignKey(to='PlagCheck.Store', related_name='suspicion_suspect')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='suspect',
            name='result',
        ),
        migrations.RemoveField(
            model_name='suspect',
            name='similar_to',
        ),
        migrations.RemoveField(
            model_name='suspect',
            name='stored_doc',
        ),
        migrations.DeleteModel(
            name='Suspect',
        ),
        migrations.RenameField(
            model_name='result',
            old_name='stored_doc',
            new_name='doc',
        ),
        migrations.RenameModel(
            old_name='Store',
            new_name='Document',
        ),
    ]
