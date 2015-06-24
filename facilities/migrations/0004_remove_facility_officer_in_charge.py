# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20150619_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='officer_in_charge',
        ),
    ]
