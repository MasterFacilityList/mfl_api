# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', '0001_drilldownview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitycoordinates',
            name='method',
            field=models.ForeignKey(blank=True, to='mfl_gis.GeoCodeMethod', help_text=b'Method used to obtain the geo codes. e.g taken with GPS device', null=True),
        ),
        migrations.AlterField(
            model_name='facilitycoordinates',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='mfl_gis.GeoCodeSource', help_text=b'where the geo code came from', null=True),
        ),
    ]
