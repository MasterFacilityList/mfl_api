# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20160406_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='town_name',
            field=models.CharField(help_text=b'The town where the entity is located e.g Nakuru', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='keph_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.KephLevel', help_text=b'The keph level of the facility', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='operation_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.FacilityStatus', help_text=b'Indicates whether the facilityhas been approved to operate, is operating, is temporarilynon-operational, or is closed down', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.Owner', help_text=b'A link to the organization that owns the facility'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='regulation_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.RegulationStatus', help_text=b'The regulatory status of the hospital', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='regulatory_body',
            field=models.ForeignKey(to='facilities.RegulatingBody', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facility',
            name='sub_county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.SubCounty', help_text=b'The sub county in which the facility has been assigned', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='town',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.Town', help_text=b'The town where the entity is located e.g Nakuru', null=True),
        ),
        migrations.AlterField(
            model_name='facilityofficer',
            name='facility',
            field=models.ForeignKey(related_name='facility_officers', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
        migrations.AlterField(
            model_name='facilityofficer',
            name='officer',
            field=models.ForeignKey(related_name='officer_facilities', on_delete=django.db.models.deletion.PROTECT, to='facilities.Officer'),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='facility',
            field=models.ForeignKey(related_name='facility_services', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.Option', null=True),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='service',
            field=models.ForeignKey(to='facilities.Service', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilityservicerating',
            name='facility_service',
            field=models.ForeignKey(related_name='facility_service_ratings', on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityService'),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ForeignKey(related_name='category_services', on_delete=django.db.models.deletion.PROTECT, to='facilities.ServiceCategory', help_text=b'The classification that the service lies in.'),
        ),
    ]
