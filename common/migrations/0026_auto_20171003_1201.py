# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_auto_20170928_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituencymapping',
            name='dhis_parent_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='countymapping',
            name='dhis_parent_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subcountymapping',
            name='dhis_parent_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wardmapping',
            name='dhis_parent_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
