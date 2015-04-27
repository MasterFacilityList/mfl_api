# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituencyboundary',
            name='mpoly',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='countyboundary',
            name='mpoly',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='wardboundary',
            name='mpoly',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worldborder',
            name='mpoly',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True),
        ),
    ]
