# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0018_countymapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countymapping',
            name='dhis_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='countymapping',
            name='dhis_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
