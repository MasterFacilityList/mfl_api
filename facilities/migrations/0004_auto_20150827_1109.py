# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20150825_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityupdates',
            name='contacts',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facilityupdates',
            name='officer_in_charge',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facilityupdates',
            name='services',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facilityupdates',
            name='units',
            field=models.TextField(null=True, blank=True),
        ),
    ]
