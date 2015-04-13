# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0008_auto_20150413_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilitygps',
            name='is_classified',
        ),
        migrations.AddField(
            model_name='facility',
            name='is_classified',
            field=models.BooleanField(default=False, help_text=b'Should the facility be visible to the public?'),
        ),
    ]
