# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('hash', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hash_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('doc_id', models.IntegerField()),
                ('text', models.TextField()),
                ('user_id', models.IntegerField(null=True)),
                ('user_name', models.CharField(null=True, max_length=100)),
                ('submission_time', models.DateTimeField(null=True)),
                ('is_revised', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Suspect',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('similarity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(default=0, choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'FILTER'), (4, 'AUTO_FILTERED'), (5, 'CITED')], max_length=2)),
                ('match_count', models.IntegerField()),
                ('result', models.ForeignKey(to='PlagCheck.Result')),
                ('similar_to', models.ForeignKey(related_name='suspected_similar_to', to='PlagCheck.Store')),
                ('stored_doc', models.ForeignKey(related_name='suspected_doc', to='PlagCheck.Store')),
            ],
        ),
        migrations.CreateModel(
            name='SuspectFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('stored_doc', models.ForeignKey(to='PlagCheck.Store')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='stored_doc',
            field=models.ForeignKey(to='PlagCheck.Store'),
        ),
        migrations.AddField(
            model_name='reference',
            name='stored_doc',
            field=models.ForeignKey(to='PlagCheck.Store'),
        ),
    ]
