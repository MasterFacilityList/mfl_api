# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20150428_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityType', help_text=b'This depends on who owns the facilty. For MOH facilities,type is the gazetted classification of the facilty.For Non-MOH check under the respective owners.'),
        ),
    ]
