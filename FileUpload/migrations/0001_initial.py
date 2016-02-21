# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import FileUpload.models


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0003_aurorauser_tags'),
        ('Elaboration', '0003_elaboration_revised_elaboration_changelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('upload_file', models.FileField(upload_to=FileUpload.models.get_upload_path)),
                ('thumbnail', models.ImageField(blank=True, upload_to=FileUpload.models.get_thumbnail_path, null=True)),
                ('elaboration', models.ForeignKey(to='Elaboration.Elaboration')),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
