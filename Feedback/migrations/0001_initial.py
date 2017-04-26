# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lane',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('hidden', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
