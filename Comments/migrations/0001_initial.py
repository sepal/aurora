# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('AuroraUser', '0003_aurorauser_tags'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('post_date', models.DateTimeField(verbose_name='date posted')),
                ('delete_date', models.DateTimeField(blank=True, verbose_name='date deleted', null=True)),
                ('edited_date', models.DateTimeField(blank=True, verbose_name='date edited', null=True)),
                ('promoted', models.BooleanField(default=False)),
                ('seen', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('visibility', models.CharField(default='public', max_length=10, choices=[('public', 'public'), ('staff', 'staff only'), ('private', 'private note')])),
                ('author', models.ForeignKey(to='AuroraUser.AuroraUser')),
                ('bookmarked_by', models.ManyToManyField(to='AuroraUser.AuroraUser', related_name='bookmarked_comments_set')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleter', models.ForeignKey(to='AuroraUser.AuroraUser', related_name='deleted_comments_set', null=True, blank=True)),
                ('parent', models.ForeignKey(to='Comments.Comment', related_name='children', null=True, blank=True)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag', through='taggit.TaggedItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision', models.BigIntegerField(default=0)),
                ('uri', models.CharField(max_length=200, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentReferenceObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentsConfig',
            fields=[
                ('key', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('value', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.BooleanField(default=True, choices=[(True, True), (False, False)])),
                ('comment', models.ForeignKey(to='Comments.Comment', related_name='votes')),
                ('voter', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('voter', 'comment')]),
        ),
        migrations.AlterUniqueTogether(
            name='commentlist',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
