# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0006_auto_20150626_1242'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='facilityofficer',
            unique_together=set([('facility', 'officer')]),
        ),
    ]
