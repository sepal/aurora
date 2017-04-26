# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0003_aurorauser_tags'),
        ('Feedback', '0003_issue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('issue', models.ForeignKey(to='Feedback.Issue')),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
