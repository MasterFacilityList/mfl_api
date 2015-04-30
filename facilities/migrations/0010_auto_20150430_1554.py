# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0009_auto_20150430_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='id_number',
            field=models.CharField(help_text=b'The  National Identity number of the officer', max_length=10, null=True, blank=True),
        ),
    ]
