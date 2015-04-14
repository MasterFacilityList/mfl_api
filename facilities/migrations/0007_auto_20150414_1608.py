# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0006_auto_20150414_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='regulatory_details',
        ),
        migrations.AlterField(
            model_name='facilityregulationstatus',
            name='facility',
            field=models.ForeignKey(related_name='regulatory_details', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
    ]
