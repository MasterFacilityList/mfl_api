# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150429_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicaladdress',
            name='postal_code',
            field=models.CharField(help_text=b'The 5 digit number for the post office address. e.g 00900', max_length=100, null=True, blank=True),
        ),
    ]
