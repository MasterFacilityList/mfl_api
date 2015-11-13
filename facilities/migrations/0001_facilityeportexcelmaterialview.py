# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'export_facilities_material_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityEportExcelMaterialView',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of the facility', max_length=100)),
                ('code', models.CharField(help_text=b'The facility code', max_length=100)),
                ('registration_number', models.CharField(help_text=b'The facilities registration_number', max_length=100)),
                ('keph_level', models.CharField(help_text=b"The facility's keph-level", max_length=100)),
                ('facility_type_name', models.CharField(help_text=b'The facility type', max_length=100)),
                ('county', models.CharField(help_text=b"Name of the facility's county", max_length=100)),
                ('constituency', models.CharField(help_text=b"The name of the facility's constituency ", max_length=100)),
                ('ward_name', models.CharField(help_text=b"Name of the facility's ward", max_length=100)),
                ('owner', models.CharField(help_text=b"The facility's owner", max_length=100)),
                ('regulatory_body_name', models.CharField(help_text=b"The name of the facility's regulator", max_length=100)),
                ('beds', models.CharField(help_text=b'The number of beds in the facility', max_length=100)),
                ('cots', models.CharField(help_text=b'The number of cots in the facility', max_length=100)),
            ],
            options={
                'db_table': 'facilities_excel_export',
                'managed': False,
            },
        ),
    ]
