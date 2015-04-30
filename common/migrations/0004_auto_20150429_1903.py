# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20150429_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicaladdress',
            name='address',
            field=models.TextField(help_text=b'This is the actual post office number of the entitye.g 6790', null=True, blank=True),
        ),
    ]
