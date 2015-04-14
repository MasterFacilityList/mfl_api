# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_facilitygps_collection_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='is_published',
            field=models.BooleanField(default=False, help_text=b'Should be True if the facility is to be seen on the public MFL site'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='is_classified',
            field=models.BooleanField(default=False, help_text=b"Should the facility geo-codes be visible to the public?Certain facilities are kept 'off-the-map'"),
        ),
    ]
