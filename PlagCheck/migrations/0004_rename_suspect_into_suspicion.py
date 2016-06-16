# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0003_result_submission_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suspicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('similarity', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=2, choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED')], default=0)),
                ('match_count', models.IntegerField()),
                ('result', models.ForeignKey(to='PlagCheck.Result')),
                ('similar_to', models.ForeignKey(related_name='suspicion_similar_to', to='PlagCheck.Store')),
                ('stored_doc', models.ForeignKey(related_name='suspicion_suspect', to='PlagCheck.Store')),
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
    ]
