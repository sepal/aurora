# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Challenge', '__first__'),
        ('Course', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(to='Course.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StackChallengeRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('challenge', models.ForeignKey(to='Challenge.Challenge')),
                ('stack', models.ForeignKey(to='Stack.Stack')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
