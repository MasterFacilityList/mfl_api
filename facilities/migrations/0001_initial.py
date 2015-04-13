# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import common.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'This is the official name of the facility', unique=True, max_length=100)),
                ('code', models.IntegerField(help_text=b'A sequential number allocated to each facility', unique=True)),
                ('description', models.TextField(help_text=b'A brief summary of the Facility')),
                ('number_of_beds', models.PositiveIntegerField(default=0, help_text=b'The number of beds that a facilty has. e.g 0')),
                ('number_of_cots', models.PositiveIntegerField(default=0, help_text=b'The number of cots that a facility has e.g 0')),
                ('open_whole_day', models.BooleanField(default=False, help_text=b'Is the facility open 24 hours a day?')),
                ('open_whole_week', models.BooleanField(default=False, help_text=b'Is the facility open the entire week?')),
                ('location_desc', models.TextField(help_text=b'This field allows a more detailed description of how tolocate the facility e.g Joy medical clinic is in Jubilee Plaza7th Floor')),
                ('is_classified', models.BooleanField(default=False, help_text=b'Should the facility be visible to the public?')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='FacilityContact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(to='common.Contact', on_delete=django.db.models.deletion.PROTECT)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacilityGPS',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('latitude', models.CharField(help_text=b'How far north or south a facility is from the equator', max_length=255)),
                ('longitude', models.CharField(help_text=b'How far east or west one a facility is from the Greenwich Meridian', max_length=255)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility', models.OneToOneField(to='facilities.Facility')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacilityRegulationStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('reason', models.TextField(help_text=b'e.g Why has a facility been suspended', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacilityService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Is the offered or not.')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(related_name='facility_services', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacilityStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'A short name respresenting the operanation status e.g OPERATIONAL', unique=True, max_length=100)),
                ('description', models.TextField(help_text=b'A short explanation of what the status entails.')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacilityType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'A short unique name for the facility type e.g DISPENSARY', unique=True, max_length=100)),
                ('sub_division', models.CharField(help_text=b'This is a further division of the facility type e.g Hospitals can be further divided into District hispitals and Provincial Hospitals.', max_length=100, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GeoCodeMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'The name of the method.', max_length=100)),
                ('description', models.TextField(help_text=b'A short description of the method', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeoCodeSource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'The name of the collecting organization', max_length=100)),
                ('description', models.TextField(help_text=b'A short summary of the collecting organization', null=True, blank=True)),
                ('abbreviation', models.CharField(help_text=b'An acronym of the collecting or e.g SAM', max_length=10)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'A short name for the job title', max_length=100)),
                ('description', models.TextField(help_text=b'A short summary of the job title')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfficerIchargeContact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Contact', help_text=b'The contact of the officer incharge may it be email,  mobile number etc')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfficerIncharge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'the name of the officer in-charge e.g Roselyne Wiyanga ', max_length=150)),
                ('registration_number', models.CharField(help_text=b'This is the licence number of the officer. e.g for a nurse use the NCK registration number.', max_length=100)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('job_title', models.ForeignKey(to='facilities.JobTitle', on_delete=django.db.models.deletion.PROTECT)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'The name of owner e.g Ministry of Health.', unique=True, max_length=100)),
                ('description', models.TextField(help_text=b'A brief summary of the owner.', null=True, blank=True)),
                ('code', models.IntegerField(help_text=b'A unique number to identify the owner.Could be up to 7 characteres long.', unique=True)),
                ('abbreviation', models.CharField(help_text=b'Short form of the name of the owner e.g Ministry of health could be shortened as MOH', max_length=10, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OwnerType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'Short unique name for a particular type of owners. e.g INDIVIDUAL', max_length=100)),
                ('description', models.TextField(help_text=b'A brief summary of the particular type of owner.', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegulatingBody',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'The name of the regulating body', unique=True, max_length=100)),
                ('abbreviation', models.CharField(help_text=b'A shortform of the name of the regulating body e.g NursingCouncil of Kenya could be abbreviated as NCK.', max_length=10, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegulationStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'A short unique name representing a state/stage of regulation e.g. PENDING_OPENING ', unique=True, max_length=100)),
                ('description', models.TextField(help_text=b"A short description of the regulation state or state e.gPENDING_OPENING could be descriped as 'waiting for the license tobegin operating' ")),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('code', models.IntegerField(unique=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'What is the name of the category? ', max_length=100)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='owner',
            name='owner_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OwnerType', help_text=b'The classification of the owner e.g INDIVIDUAL'),
        ),
        migrations.AddField(
            model_name='owner',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='officerichargecontact',
            name='officer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OfficerIncharge', help_text=b'The is the officer in charge'),
        ),
        migrations.AddField(
            model_name='officerichargecontact',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='service',
            field=models.ForeignKey(to='facilities.Service', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='regulation_status',
            field=models.ForeignKey(to='facilities.RegulationStatus', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitygps',
            name='method',
            field=models.ForeignKey(help_text=b'Method used to obtain the geo codes. e.g taken with GPS device', to='facilities.GeoCodeMethod'),
        ),
        migrations.AddField(
            model_name='facilitygps',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.GeoCodeSource', help_text=b'where the geo code came from'),
        ),
        migrations.AddField(
            model_name='facilitygps',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facility',
            name='facility_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityType', help_text=b'This depends on who owns the facilty. For MOH facilities,type is the gazetted classification of the facilty.For Non-MOH check under the respective owners.'),
        ),
        migrations.AddField(
            model_name='facility',
            name='operation_status',
            field=models.OneToOneField(to='facilities.FacilityStatus', help_text=b'Indicates whether the facilityhas been approved to operate, is operating, is temporarilynon-operational, or is closed down'),
        ),
        migrations.AddField(
            model_name='facility',
            name='owner',
            field=models.ForeignKey(to='facilities.Owner'),
        ),
        migrations.AddField(
            model_name='facility',
            name='regulating_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.RegulatingBody', help_text=b'The National Regulatory Body responsible for licensing or gazettement of the facility', null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='regulation_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.RegulationStatus', help_text=b'Indicates whether the facility has been approved by the respective National Regulatory Body.', null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='sub_county',
            field=models.ForeignKey(to='common.SubCounty', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facility',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='facilitytype',
            unique_together=set([('name', 'sub_division')]),
        ),
    ]
