# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'set_facility_code_sequence_min_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulatingbodycontact',
            name='regulating_body',
            field=models.ForeignKey(related_name='reg_contacts', to='facilities.RegulatingBody'),
        ),
        migrations.AlterField(
            model_name='regulationstatus',
            name='description',
            field=models.TextField(help_text=b"A short description of the regulation state or state e.gPENDING_LICENSING could be descriped as 'waiting for the license tobegin operating' ", null=True, blank=True),
        ),
    ]
