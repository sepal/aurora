# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stack', '0005_stack_challenges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stack',
            name='challenges',
        ),
    ]
