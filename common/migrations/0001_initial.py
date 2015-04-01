# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=254)),
                ('town', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('nearest_town', models.CharField(max_length=100)),
                ('landline', models.CharField(max_length=100)),
                ('fax', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('county', models.ForeignKey(to='common.County')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('district', models.ForeignKey(to='common.District')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('job', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('subjet', models.CharField(max_length=255)),
                ('comment', models.TextField()),
            ],
            options={
                'verbose_name': 'Feedback from users',
                'verbose_name_plural': 'Feedback from users',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('division', models.ForeignKey(to='common.Division')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('location', models.ForeignKey(to='common.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='county',
            name='Province',
            field=models.ForeignKey(to='common.Province'),
        ),
        migrations.AddField(
            model_name='constituency',
            name='county',
            field=models.ForeignKey(to='common.County'),
        ),
    ]
