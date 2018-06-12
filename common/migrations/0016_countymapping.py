# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_apiauthentication'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountyMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('mfl_name', models.CharField(max_length=255)),
                ('mfl_code', models.IntegerField(default=0)),
                ('dhis_name', models.CharField(max_length=255)),
                ('dhis_id', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
                'verbose_name_plural': 'county_mappings',
            },
        ),
    ]
