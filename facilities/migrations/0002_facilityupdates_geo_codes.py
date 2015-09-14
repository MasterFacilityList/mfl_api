# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'set_facility_code_sequence_min_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityupdates',
            name='geo_codes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
