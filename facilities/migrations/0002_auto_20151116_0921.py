# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_facilityeportexcelmaterialview'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityExportExcelMaterialView',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of the facility', max_length=100)),
                ('code', models.IntegerField(help_text=b'The facility code')),
                ('registration_number', models.CharField(help_text=b'The facilities registration_number', max_length=100)),
                ('keph_level_name', models.UUIDField(help_text=b"The facility's keph-level", null=True, blank=True)),
                ('facility_type_name', models.CharField(help_text=b'The facility type', max_length=100)),
                ('county', models.UUIDField(help_text=b"Name of the facility's county", null=True, blank=True)),
                ('constituency', models.UUIDField(help_text=b"The name of the facility's constituency ", null=True, blank=True)),
                ('owner_name', models.CharField(help_text=b"The facility's owner", max_length=100)),
                ('regulatory_body_name', models.CharField(help_text=b"The name of the facility's regulator", max_length=100)),
                ('beds', models.IntegerField(help_text=b'The number of beds in the facility')),
                ('cots', models.IntegerField(help_text=b'The number of cots in the facility')),
                ('search', models.CharField(help_text=b'A dummy search field', max_length=255, null=True, blank=True)),
                ('county_name', models.CharField(max_length=100, null=True, blank=True)),
                ('constituency_name', models.CharField(max_length=100, null=True, blank=True)),
                ('ward_name', models.CharField(max_length=100, null=True, blank=True)),
                ('keph_level', models.CharField(max_length=100, null=True, blank=True)),
                ('facility_type', models.CharField(max_length=100, null=True, blank=True)),
                ('owner_type', models.CharField(max_length=100, null=True, blank=True)),
                ('owner', models.UUIDField(null=True, blank=True)),
                ('operation_status', models.UUIDField(null=True, blank=True)),
                ('operation_status_name', models.CharField(max_length=100, null=True, blank=True)),
                ('open_whole_day', models.BooleanField(default=False, help_text=b'Does the facility operate 24 hours a day')),
                ('open_public_holidays', models.BooleanField(default=False, help_text=b'Is the facility open on public holidays?')),
                ('open_weekends', models.BooleanField(default=False, help_text=b'Is the facility_open during weekends?')),
                ('open_late_night', models.BooleanField(default=False, help_text=b'Indicates if a facility is open late night e.g up-to 11 pm')),
                ('services', django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.UUIDField(null=True, blank=True), blank=True)),
                ('categories', django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.UUIDField(null=True, blank=True), blank=True)),
            ],
            options={
                'db_table': 'facilities_excel_export',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='facilitystatus',
            name='name',
            field=models.CharField(help_text=b'A short name representing the operation status e.g OPERATIONAL', unique=True, max_length=100),
        ),
    ]
