# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0008_courseuserrelation_positive_completion_possible'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('order', models.PositiveIntegerField()),
                ('course', models.ManyToManyField(to='Course.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
