# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0004_review_extra_review_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewevaluation',
            name='appraisal',
            field=models.CharField(choices=[('P', 'Helpful Review'), ('D', 'Good Review'), ('B', 'Bad Review'), ('N', 'Negative Review')], default='D', max_length=1),
        ),
    ]
