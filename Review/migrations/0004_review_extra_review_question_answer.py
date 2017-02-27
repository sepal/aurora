# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0003_auto_20160517_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='extra_review_question_answer',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
