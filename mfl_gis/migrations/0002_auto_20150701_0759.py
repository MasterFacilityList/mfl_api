# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitycoordinates',
            name='facility',
            field=models.OneToOneField(related_name='facility_coordinates_through', to='facilities.Facility'),
        ),
    ]
