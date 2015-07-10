# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0009_auto_20150709_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regulationstatus',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='regulationstatus',
            name='regulated',
        ),
        migrations.AddField(
            model_name='facility',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facility',
            name='regulated',
            field=models.BooleanField(default=False),
        ),
    ]
