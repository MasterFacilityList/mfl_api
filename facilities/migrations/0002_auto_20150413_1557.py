# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150413_1556'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategory',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servicecategory',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='regulationstatus',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='regulationstatus',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='regulatingbody',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='regulatingbody',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ownertype',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ownertype',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='owner',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='owner',
            name='owner_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OwnerType', help_text=b'The classification of the owner e.g INDIVIDUAL'),
        ),
        migrations.AddField(
            model_name='owner',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='officerincharge',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='officerincharge',
            name='job_title',
            field=models.ForeignKey(to='facilities.JobTitle', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='officerincharge',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='officerichargecontact',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Contact', help_text=b'The contact of the officer incharge may it be email,  mobile number etc'),
        ),
        migrations.AddField(
            model_name='officerichargecontact',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='officerichargecontact',
            name='officer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OfficerIncharge', help_text=b'The is the officer in charge'),
        ),
        migrations.AddField(
            model_name='officerichargecontact',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='geocodesource',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='geocodesource',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='geocodemethod',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='geocodemethod',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitytype',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitytype',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitystatus',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitystatus',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='facility',
            field=models.ForeignKey(related_name='facility_services', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='service',
            field=models.ForeignKey(to='facilities.Service', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='facility',
            field=models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='regulation_status',
            field=models.ForeignKey(to='facilities.RegulationStatus', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitygps',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitygps',
            name='facility',
            field=models.OneToOneField(to='facilities.Facility'),
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
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitycontact',
            name='contact',
            field=models.ForeignKey(to='common.Contact', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilitycontact',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilitycontact',
            name='facility',
            field=models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilitycontact',
            name='updated_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facility',
            name='created_by',
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
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
            field=models.ForeignKey(related_name='+', default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='facilitytype',
            unique_together=set([('name', 'sub_division')]),
        ),
    ]
