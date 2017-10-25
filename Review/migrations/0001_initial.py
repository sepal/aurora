# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('AuroraUser', '0003_aurorauser_tags'),
        ('Elaboration', '0004_elaboration_most_helpful_other_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('submission_time', models.DateTimeField(null=True)),
                ('appraisal', models.CharField(choices=[('N', 'Not even trying'), ('F', 'Fail'), ('S', 'Success'), ('A', 'Awesome')], max_length=1, null=True)),
                ('elaboration', models.ForeignKey(to='Elaboration.Elaboration', on_delete=models.CASCADE)),
                ('reviewer', models.ForeignKey(to='AuroraUser.AuroraUser', on_delete=models.CASCADE)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.', through='taggit.TaggedItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('candidate_offset_min', models.IntegerField(default=0)),
                ('candidate_offset_max', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewEvaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('appraisal', models.CharField(default='D', choices=[('D', 'Average Review'), ('N', 'Flag this review as meaningless or offensive'), ('P', 'This review was helpful')], max_length=1)),
                ('review', models.ForeignKey(to='Review.Review', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
