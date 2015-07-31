# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'set_facility_code_sequence_min_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityunit',
            name='facility',
            field=models.ForeignKey(related_name='facility_units', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
    ]
