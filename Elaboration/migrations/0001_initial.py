# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('Challenge', '__first__'),
        ('taggit', '0001_initial'),
        ('AuroraUser', '0003_aurorauser_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elaboration',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('elaboration_text', models.TextField(default='')),
                ('submission_time', models.DateTimeField(null=True)),
                ('challenge', models.ForeignKey(to='Challenge.Challenge', on_delete=models.CASCADE)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', verbose_name='Tags', through='taggit.TaggedItem', help_text='A comma-separated list of tags.')),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
