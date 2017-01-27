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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('image', models.ImageField(upload_to=Slides.models.Slide.upload_location)),
                ('text_content', models.TextField(blank=True, null=True)),
                ('tags', models.CharField(max_length=240, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlideStack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('tags', models.CharField(max_length=240, blank=True, null=True)),
                ('categories', models.TextField(max_length=500, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='slide',
            name='slide_stack',
            field=models.ForeignKey(to='Slides.SlideStack'),
            preserve_default=True,
        ),
    ]
