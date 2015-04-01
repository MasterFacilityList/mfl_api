# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityUnits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('is_classified', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('facility_type', models.CharField(max_length=100, choices=[(b'DISPENSARY', b'dispensary'), (b'HEALTH_CENTER', b'Health Center'), (b'LEVEL_1', b'Level 1 facility'), (b'LEVEL_2', b'Level 2 facility'), (b'LEVEL_3', b'Level 3 facility'), (b'LEVEL_4', b'Level 4 facility'), (b'LEVEL_5', b'Level 5 facility')])),
                ('number_of_beds', models.PositiveIntegerField(default=0)),
                ('number_of_cots', models.PositiveIntegerField(default=0)),
                ('open_whole_day', models.BooleanField(default=False)),
                ('open_whole_week', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=50, choices=[(b'OPERATIONAL', b'Operations are running normally'), (b'NOT_OPERATIONAL', b'The facility is not operating')])),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('code', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='facility',
            name='owner',
            field=models.ForeignKey(to='facilities.Owner'),
        ),
        migrations.AddField(
            model_name='facility',
            name='services',
            field=models.ManyToManyField(to='facilities.Service'),
        ),
        migrations.AddField(
            model_name='facility',
            name='sub_location',
            field=models.ForeignKey(to='common.SubLocation'),
        ),
    ]
