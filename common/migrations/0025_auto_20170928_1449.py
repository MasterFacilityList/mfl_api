# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0024_wardmapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituencymapping',
            name='constituency_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='constituencymapping',
            name='county_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subcountymapping',
            name='county_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subcountymapping',
            name='sub_county_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='wardmapping',
            name='sub_county_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='wardmapping',
            name='ward_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
