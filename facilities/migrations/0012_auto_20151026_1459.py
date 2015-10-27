# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0011_auto_20151027_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityservice',
            name='is_cancelled',
            field=models.BooleanField(default=False, help_text=b'Indicates whether a service has been canceled by the CHRIO'),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='is_confirmed',
            field=models.BooleanField(default=False, help_text=b'Indicates whether a service has been approved by the CHRIO'),
        ),
        migrations.AlterField(
            model_name='facilitytype',
            name='sub_division',
            field=models.CharField(help_text=b'This is a further division of the facility type e.g Hospitals can be further divided into District hospitals and Provincial Hospitals.', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='facilityupgrade',
            name='is_cancelled',
            field=models.BooleanField(default=False, help_text=b'Indicates whether a facility upgrade or downgrade has beencanceled or not'),
        ),
        migrations.AlterField(
            model_name='kephlevel',
            name='is_facility_level',
            field=models.BooleanField(default=True, help_text=b'Is the KEPH level applicable to facilities'),
        ),
        migrations.AlterField(
            model_name='officer',
            name='registration_number',
            field=models.CharField(help_text=b'This is the license number of the officer. e.g for a nurse use the NCK registration number.', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='officercontact',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Contact', help_text=b'The contact of the officer in-charge may it be email,  mobile number etc'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='code',
            field=common.fields.SequenceField(help_text=b'A unique number to identify the owner.Could be up to 7 characters long.', unique=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='regulationstatus',
            name='description',
            field=models.TextField(help_text=b"A short description of the regulation state or state e.gPENDING_LICENSING could be described as 'waiting for the license tobegin operating' ", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='regulationstatus',
            name='is_default',
            field=models.BooleanField(default=False, help_text=b'The default regulation status for facilities'),
        ),
        migrations.AlterField(
            model_name='regulationstatus',
            name='next_status',
            field=models.ForeignKey(related_name='next_state', blank=True, to='facilities.RegulationStatus', help_text=b'The regulation_status succeeding this regulation status.', null=True),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='keph_level',
            field=models.ForeignKey(blank=True, to='facilities.KephLevel', help_text=b'The KEPH level at which certain services should be offered', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='regulatorybodyuser',
            unique_together=set([]),
        ),
    ]
