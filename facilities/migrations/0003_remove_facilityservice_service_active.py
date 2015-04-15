# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150415_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilityservice',
            name='service_active',
        ),
    ]
