# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Feedback', '0004_upvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='user_agent',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
