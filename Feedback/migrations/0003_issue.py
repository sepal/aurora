# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0004_courseuserrelation_active'),
        ('AuroraUser', '0003_aurorauser_tags'),
        ('Feedback', '0002_auto_20160619_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=25, choices=[('bug', 'Bug'), ('feature_request', 'Feature Request'), ('feedback', 'Feedback'), ('security', 'Security')])),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(to='AuroraUser.AuroraUser', on_delete=models.CASCADE)),
                ('course', models.ForeignKey(to='Course.Course', on_delete=models.CASCADE)),
                ('lane', models.ForeignKey(to='Feedback.Lane', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
