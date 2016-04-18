# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20160411_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityunit',
            name='registration_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
