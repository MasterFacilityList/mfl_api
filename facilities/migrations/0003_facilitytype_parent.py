# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_facility_county'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitytype',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.FacilityType', null=True),
        ),
    ]
