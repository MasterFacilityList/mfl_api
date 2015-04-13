# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_auto_20150413_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituency',
            name='code',
            field=models.CharField(help_text=b'A unique_code 4 digit number representing the region.', unique=True, max_length=100, editable=False),
        ),
        migrations.AlterField(
            model_name='county',
            name='code',
            field=models.CharField(help_text=b'A unique_code 4 digit number representing the region.', unique=True, max_length=100, editable=False),
        ),
        migrations.AlterField(
            model_name='subcounty',
            name='code',
            field=models.CharField(help_text=b'A unique_code 4 digit number representing the region.', unique=True, max_length=100, editable=False),
        ),
    ]
