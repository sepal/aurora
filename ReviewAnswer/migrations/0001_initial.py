# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0005_auto_20170227_1416'),
        ('ReviewQuestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('text', models.TextField(null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(to='Review.Review')),
                ('review_question', models.ForeignKey(to='ReviewQuestion.ReviewQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
