# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'set_facility_code_sequence_min_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilitytype',
            name='code',
        ),
        migrations.RemoveField(
            model_name='kephlevel',
            name='code',
        ),
        migrations.RemoveField(
            model_name='ownertype',
            name='code',
        ),
        migrations.RemoveField(
            model_name='regulatingbody',
            name='code',
        ),
        migrations.RemoveField(
            model_name='regulationstatus',
            name='code',
        ),
    ]
