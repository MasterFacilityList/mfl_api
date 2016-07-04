# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20160517_0934'),
        ('facilities', '0001_auto_20160516_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.County', null=True),
        ),
    ]
