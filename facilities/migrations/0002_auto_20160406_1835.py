# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_auto_20160328_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityunit',
            name='license_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='facilitytype',
            name='sub_division',
            field=models.CharField(help_text=b'Parent of the facility type e.g sub-district hospitals are under Hospitals.', max_length=100, null=True, blank=True),
        ),
    ]
