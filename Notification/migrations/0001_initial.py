# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0003_aurorauser_tags'),
        ('Course', '0008_courseuserrelation_positive_completion_possible'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedToken',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('token', models.CharField(max_length=100, default=uuid.uuid4, unique=True, blank=True)),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('text', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=100, default='/static/img/info.jpg')),
                ('link', models.CharField(max_length=100, default='')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='Course.Course')),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
