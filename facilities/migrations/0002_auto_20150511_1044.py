# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityunit',
            name='regulating_body',
            field=models.ForeignKey(blank=True, to='facilities.RegulatingBody', null=True),
        ),
        migrations.AlterField(
            model_name='facilityunit',
            name='regulation_status',
            field=models.ForeignKey(blank=True, to='facilities.RegulationStatus', null=True),
        ),
    ]
