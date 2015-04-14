# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20150414_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facilityregulationstatus',
            options={'ordering': ('-created',)},
        ),
        migrations.RemoveField(
            model_name='facility',
            name='regulation_status',
        ),
    ]
