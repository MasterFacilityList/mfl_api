# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_facilityupgrade_keph_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='open_late_night',
            field=models.BooleanField(default=False, help_text=b'Indicates if a facility is open late night e.g upto 11 pm'),
        ),
    ]
