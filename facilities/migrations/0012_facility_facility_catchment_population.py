# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0011_auto_20151027_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='facility_catchment_population',
            field=models.IntegerField(help_text=b'The population size which the facility serves', null=True, blank=True),
        ),
    ]
