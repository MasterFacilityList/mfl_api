# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150818_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityupgrade',
            name='current_facility_type_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facilityupgrade',
            name='current_keph_level_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
