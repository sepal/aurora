# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Challenge', '0001_initial'),
        ('Stack', '0004_auto_20160118_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='stack',
            name='challenges',
            field=models.ManyToManyField(through='Stack.StackChallengeRelation', to='Challenge.Challenge'),
            preserve_default=True,
        ),
    ]
