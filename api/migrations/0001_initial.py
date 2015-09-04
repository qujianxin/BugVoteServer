# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administration',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='BugRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('information', models.TextField()),
                ('bonus', models.PositiveIntegerField(default=0)),
                ('have_seen', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='BugType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True)),
                ('context', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('desc', models.TextField(blank=True, default='#')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.TextField()),
                ('author', models.CharField(max_length=40)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('context', models.TextField()),
            ],
            options={
                'ordering': ('-time',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('phone_number', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=40)),
                ('school', models.CharField(max_length=40)),
                ('major', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bug_number', models.PositiveIntegerField(default=0)),
                ('bonus', models.PositiveIntegerField(default=0)),
                ('rank', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='config',
            name='images',
            field=models.ManyToManyField(blank=True, to='api.ImageItem'),
        ),
        migrations.AddField(
            model_name='bugrecord',
            name='bug_type',
            field=models.ForeignKey(to='api.BugType'),
        ),
        migrations.AddField(
            model_name='bugrecord',
            name='commit_person',
            field=models.ForeignKey(to='api.User'),
        ),
    ]
