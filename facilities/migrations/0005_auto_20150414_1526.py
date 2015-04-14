# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20150414_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='parent',
            field=models.ForeignKey(blank=True, to='facilities.Facility', help_text=b'Indicates the umbrella facility of a facility', null=True),
        ),
    ]
