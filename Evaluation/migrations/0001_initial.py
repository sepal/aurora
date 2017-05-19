# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0003_aurorauser_tags'),
        ('Elaboration', '0005_auto_20170216_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('evaluation_text', models.TextField()),
                ('evaluation_points', models.IntegerField(default=0)),
                ('submission_time', models.DateTimeField(null=True)),
                ('lock_time', models.DateTimeField(null=True)),
                ('submission', models.ForeignKey(to='Elaboration.Elaboration')),
                ('tutor', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
