# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('AuroraUser', '0003_aurorauser_tags'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField()),
                ('post_date', models.DateTimeField(verbose_name='date posted')),
                ('delete_date', models.DateTimeField(blank=True, verbose_name='date deleted', null=True)),
                ('edited_date', models.DateTimeField(blank=True, verbose_name='date edited', null=True)),
                ('promoted', models.BooleanField(default=False)),
                ('seen', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('visibility', models.CharField(choices=[('public', 'public'), ('staff', 'staff only'), ('private', 'private note')], default='public', max_length=10)),
                ('author', models.ForeignKey(to='AuroraUser.AuroraUser')),
                ('bookmarked_by', models.ManyToManyField(to='AuroraUser.AuroraUser', related_name='bookmarked_comments_set')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('deleter', models.ForeignKey(blank=True, to='AuroraUser.AuroraUser', related_name='deleted_comments_set', null=True)),
                ('parent', models.ForeignKey(blank=True, to='Comments.Comment', related_name='children', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.', through='taggit.TaggedItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('revision', models.BigIntegerField(default=0)),
                ('uri', models.CharField(null=True, max_length=200)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentsConfig',
            fields=[
                ('key', models.CharField(serialize=False, primary_key=True, max_length=30)),
                ('value', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('direction', models.BooleanField(choices=[(True, True), (False, False)], default=True)),
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
