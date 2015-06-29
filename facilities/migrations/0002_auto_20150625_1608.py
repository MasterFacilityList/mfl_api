# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, editable=False, to='facilities.FacilityType', help_text=b'This depends on who owns the facility. For MOH facilities,type is the gazetted classification of the facility.For Non-MOH check under the respective owners.'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='operation_status',
            field=models.ForeignKey(blank=True, editable=False, to='facilities.FacilityStatus', help_text=b'Indicates whether the facilityhas been approved to operate, is operating, is temporarilynon-operational, or is closed down', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='regulatory_body',
            field=models.ForeignKey(blank=True, editable=False, to='facilities.RegulatingBody', null=True),
        ),
    ]
