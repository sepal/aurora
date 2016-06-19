# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0003_aurorauser_tags'),
        ('Course', '0004_courseuserrelation_active'),
        ('Feedback', '0002_auto_20160619_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('post_date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(to='AuroraUser.AuroraUser')),
                ('course', models.ForeignKey(to='Course.Course')),
                ('lane', models.ForeignKey(to='Feedback.Lane')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
