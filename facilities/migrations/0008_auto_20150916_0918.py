# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_auto_20150916_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityunit',
            name='unit',
            field=models.ForeignKey(related_name='unit_facilities', on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityDepartment'),
        ),
    ]
