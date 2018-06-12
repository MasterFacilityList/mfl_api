# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'update_material_view_with_updated_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.Ward', help_text=b'County ward in which the facility is located', null=True),
        ),
        migrations.AlterField(
            model_name='facilityapproval',
            name='facility',
            field=models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilitydepartment',
            name='regulatory_body',
            field=models.ForeignKey(to='facilities.RegulatingBody', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilityoperationstate',
            name='facility',
            field=models.ForeignKey(related_name='facility_operation_states', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
        migrations.AlterField(
            model_name='facilityoperationstate',
            name='operation_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityStatus', help_text=b'Indicates whether the facilityhas been approved to operate, is operating, is temporarilynon-operational, or is closed down'),
        ),
        migrations.AlterField(
            model_name='facilityunitregulation',
            name='facility_unit',
            field=models.ForeignKey(related_name='regulations', on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityUnit'),
        ),
        migrations.AlterField(
            model_name='facilityupgrade',
            name='facility',
            field=models.ForeignKey(related_name='facility_upgrades', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
        migrations.AlterField(
            model_name='facilityupgrade',
            name='facility_type',
            field=models.ForeignKey(to='facilities.FacilityType', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='facilityupgrade',
            name='keph_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.KephLevel', null=True),
        ),
        migrations.AlterField(
            model_name='facilityupgrade',
            name='reason',
            field=models.ForeignKey(to='facilities.FacilityLevelChangeReason', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='regulatingbodycontact',
            name='contact',
            field=models.ForeignKey(to='common.Contact', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='regulatingbodycontact',
            name='regulating_body',
            field=models.ForeignKey(related_name='reg_contacts', on_delete=django.db.models.deletion.PROTECT, to='facilities.RegulatingBody'),
        ),
        migrations.AlterField(
            model_name='regulatorsync',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityType', help_text=b'The type of the facility e.g Medical Clinic'),
        ),
        migrations.AlterField(
            model_name='regulatorsync',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.Owner', help_text=b'The owner of the facility'),
        ),
        migrations.AlterField(
            model_name='regulatorsync',
            name='regulatory_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.RegulatingBody', help_text=b'The regulatory body the record came from'),
        ),
        migrations.AlterField(
            model_name='regulatorybodyuser',
            name='regulatory_body',
            field=models.ForeignKey(to='facilities.RegulatingBody', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='regulatorybodyuser',
            name='user',
            field=models.ForeignKey(related_name='regulatory_users', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='service',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OptionGroup', help_text=b'The option group containing service options'),
        ),
        migrations.AlterField(
            model_name='service',
            name='keph_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.KephLevel', help_text=b'The KEPH level at which the service ought to be offered', null=True),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='parent',
            field=models.ForeignKey(related_name='sub_categories', on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.ServiceCategory', help_text=b'The parent category under which the category falls', null=True),
        ),
    ]
