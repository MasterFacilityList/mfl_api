# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0006_facilityregulationstatus_license_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='attributes',
            field=django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.Ward', help_text=b'County ward in which the facility is located', null=True),
        ),
    ]
