# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituencyboundary',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='countyboundary',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facilitycoordinates',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='geocodemethod',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='geocodesource',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wardboundary',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='worldborder',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
