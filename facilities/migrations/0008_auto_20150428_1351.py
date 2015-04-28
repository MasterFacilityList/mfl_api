# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore

from django.contrib.postgres.operations import HStoreExtension
class Migration(migrations.Migration, HStoreExtension):

    dependencies = [
        ('facilities', '0007_auto_20150428_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='attributes',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=b'{"null": "true"}'),
        ),
    ]
