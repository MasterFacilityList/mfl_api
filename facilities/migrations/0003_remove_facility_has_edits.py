# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_facilityupdates_cancelled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='has_edits',
        ),
    ]
