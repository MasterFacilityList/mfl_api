# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'update_export_facilities_material_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='license_number',
            field=models.CharField(help_text=b'The license number given to the hospital by the regulator', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='regulation_status',
            field=models.ForeignKey(blank=True, to='facilities.RegulationStatus', help_text=b'The regulatory status of the hospital', null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='date_established',
            field=models.DateField(help_text=b'The date when the facility became operational', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='regulatingbody',
            name='abbreviation',
            field=models.CharField(help_text=b'A short-form of the name of the regulating body e.g NursingCouncil of Kenya could be abbreviated as NCK.', max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='regulatingbody',
            name='default_status',
            field=models.ForeignKey(blank=True, to='facilities.RegulationStatus', help_text=b'The default status for the facilities regulated by the particular regulator', null=True),
        ),
        migrations.AlterField(
            model_name='regulatingbody',
            name='regulation_verb',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
