# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Challenge.models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0004_courseuserrelation_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('points', models.IntegerField(null=True)),
                ('image', models.ImageField(blank=True, upload_to=Challenge.models.challenge_image_path, null=True)),
                ('accepted_files', models.CharField(blank=True, max_length=100, default='image/*,application/pdf')),
                ('course', models.ForeignKey(to='Course.Course')),
                ('prerequisite', models.ForeignKey(blank=True, null=True, to='Challenge.Challenge')),
            ],
        ),
    ]
