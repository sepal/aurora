# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elaboration_id', models.IntegerField()),
                ('text', models.TextField()),
                ('user_id', models.IntegerField(null=True)),
                ('user_name', models.CharField(max_length=100, null=True)),
                ('submission_time', models.DateTimeField(null=True)),
                ('is_revised', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=255, db_index=True)),
                ('suspect_doc', models.ForeignKey(to='PlagCheck.Document')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hash_count', models.IntegerField()),
                ('submission_time', models.DateTimeField()),
                ('doc', models.ForeignKey(to='PlagCheck.Document')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suspicion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED')], max_length=2, default=0)),
                ('match_count', models.IntegerField()),
                ('result', models.ForeignKey(to='PlagCheck.Result')),
                ('similar_doc', models.ForeignKey(related_name='suspicion_similar', to='PlagCheck.Document')),
                ('suspect_doc', models.ForeignKey(related_name='suspicion_suspect', to='PlagCheck.Document')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
    ]
