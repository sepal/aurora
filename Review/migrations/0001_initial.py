# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('AuroraUser', '0005_auto_20160425_0912'),
        ('Elaboration', '0004_elaboration_most_helpful_other_user'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('submission_time', models.DateTimeField(null=True)),
                ('appraisal', models.CharField(choices=[('N', 'Not even trying'), ('F', 'Fail'), ('S', 'Success'), ('A', 'Awesome')], max_length=1, null=True)),
                ('elaboration', models.ForeignKey(to='Elaboration.Elaboration')),
                ('reviewer', models.ForeignKey(to='AuroraUser.AuroraUser')),
                ('tags', taggit.managers.TaggableManager(verbose_name='Tags', help_text='A comma-separated list of tags.', to='taggit.Tag', through='taggit.TaggedItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReviewConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('appraisal', models.CharField(choices=[('D', 'Average Review'), ('N', 'Flag this review as meaningless or offensive'), ('P', 'This review was helpful')], max_length=1, default='D')),
                ('review', models.ForeignKey(to='Review.Review')),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
