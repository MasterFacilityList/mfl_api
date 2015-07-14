# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', '0002_auto_20150701_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitycoordinates',
            name='collection_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
