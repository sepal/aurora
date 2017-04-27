# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0008_courseuserrelation_positive_completion_possible'),
        ('Slides', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slidestack',
            name='course',
            field=models.ForeignKey(to='Course.Course', default=1, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
