# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0008_auto_20150916_0918'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='facilitycontact',
            unique_together=set([('facility', 'contact')]),
        ),
    ]
