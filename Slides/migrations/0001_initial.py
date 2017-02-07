# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import Slides.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to=Slides.models.Slide.upload_location)),
                ('text_content', models.TextField(null=True, blank=True)),
                ('tags', models.CharField(max_length=240, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlideStack',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('tags', models.CharField(max_length=240, null=True, blank=True)),
                ('categories', models.TextField(max_length=500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
