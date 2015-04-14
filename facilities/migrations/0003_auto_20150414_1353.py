# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', 'custom_common_model_sequences'),
        ('facilities', '0002_auto_20150414_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='regulating_body',
        ),
        migrations.AddField(
            model_name='facility',
            name='contacts',
            field=models.ManyToManyField(help_text=b'Facility contacts - email, phone, fax, postal etc', to='common.Contact', through='facilities.FacilityContact'),
        ),
        migrations.AddField(
            model_name='facility',
            name='officer_in_charge',
            field=models.ForeignKey(default='2a86bb36-4e06-484b-a7c5-31c8c576b31d', to='facilities.OfficerIncharge', help_text=b'The officer in charge of the facility'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facility',
            name='regulatory_details',
            field=models.ManyToManyField(help_text=b'Regulatory bodies with interest in the facility', to='facilities.RegulatingBody', through='facilities.FacilityRegulationStatus'),
        ),
        migrations.AddField(
            model_name='facility',
            name='services',
            field=models.ManyToManyField(help_text=b'Services offered at the facility', to='facilities.Service', through='facilities.FacilityService'),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='regulating_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default='2a86bb36-4e06-484b-a7c5-31c8c576b31d', to='facilities.RegulatingBody'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='officerincharge',
            name='contacts',
            field=models.ManyToManyField(help_text=b'Personal contacts of the officer in charge', to='common.Contact', through='facilities.OfficerInchargeContact'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='owner',
            field=models.ForeignKey(help_text=b'A link to the organization that owns the facility', to='facilities.Owner'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Ward', help_text=b'County ward in which the facility is located'),
        ),
    ]
