# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150428_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='description',
            field=models.TextField(help_text=b'A brief summary of the Facility', null=True, blank=True),
        ),
    ]
