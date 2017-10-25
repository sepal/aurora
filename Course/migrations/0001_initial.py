# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0003_aurorauser_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('short_title', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField()),
                ('course_number', models.CharField(max_length=100, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseUserRelation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('course', models.ForeignKey(to='Course.Course', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
