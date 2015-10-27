# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityunit',
            name='unit',
            field=models.ForeignKey(related_name='unit_facilities', on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.FacilityDepartment', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='facilityunit',
            unique_together=set([('facility', 'unit')]),
        ),
        migrations.RemoveField(
            model_name='facilityunit',
            name='description',
        ),
        migrations.RemoveField(
            model_name='facilityunit',
            name='name',
        ),
        migrations.RemoveField(
            model_name='facilityunit',
            name='regulating_body',
        ),
    ]
