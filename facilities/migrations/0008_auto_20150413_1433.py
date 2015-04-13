# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityType', help_text=b'This depends on who owns the facilty. For MOH facilities,type is the gazetted classification of the facilty.For Non-MOH check under the respective owners.'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='regulating_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.RegulatingBody', help_text=b'The National Regulatory Body responsible for licensing or gazettement of the facility', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='regulation_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.RegulationStatus', help_text=b'Indicates whether the facility has been approved by the respective National Regulatory Body.', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='sub_county',
            field=models.ForeignKey(to='common.SubCounty', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilitycontact',
            name='contact',
            field=models.ForeignKey(to='common.Contact', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilitycontact',
            name='facility',
            field=models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilitygps',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.GeoCodeSource', help_text=b'where the geo code came from'),
        ),
        migrations.AlterField(
            model_name='facilityregulationstatus',
            name='facility',
            field=models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilityregulationstatus',
            name='regulation_status',
            field=models.ForeignKey(to='facilities.RegulationStatus', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='facility',
            field=models.ForeignKey(related_name='facility_services', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='service',
            field=models.ForeignKey(to='facilities.Service', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='officerichargecontact',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Contact', help_text=b'The contact of the officer incharge may it be email,  mobile number etc'),
        ),
        migrations.AlterField(
            model_name='officerichargecontact',
            name='officer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OfficerIncharge', help_text=b'The is the officer in charge'),
        ),
        migrations.AlterField(
            model_name='officerincharge',
            name='job_title',
            field=models.ForeignKey(to='facilities.JobTitle', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='owner',
            name='owner_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OwnerType', help_text=b'The classification of the owner e.g INDIVIDUAL'),
        ),
    ]
