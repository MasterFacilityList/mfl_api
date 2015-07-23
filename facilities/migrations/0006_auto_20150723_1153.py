# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_facility_open_late_night'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityunit',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='facilityunit',
            unique_together=set([('facility', 'name')]),
        ),
    ]
