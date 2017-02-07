# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Slides', '0002_slidestack_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='slide_stack',
            field=models.ForeignKey(default=3, to='Slides.SlideStack'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slidestack',
            name='course',
            field=models.ForeignKey(to='Course.Course'),
        ),
    ]
