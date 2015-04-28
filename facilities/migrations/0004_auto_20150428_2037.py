# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20150428_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='operation_status',
            field=models.ForeignKey(blank=True, to='facilities.FacilityStatus', help_text=b'Indicates whether the facilityhas been approved to operate, is operating, is temporarilynon-operational, or is closed down', null=True),
        ),
    ]
