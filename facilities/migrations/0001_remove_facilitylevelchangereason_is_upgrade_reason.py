# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'set_facility_code_sequence_min_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilitylevelchangereason',
            name='is_upgrade_reason',
        ),
    ]
