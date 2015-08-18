# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_auto_20150817_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='physical_address',
        ),
        migrations.AddField(
            model_name='facility',
            name='closed',
            field=models.BooleanField(default=False, help_text=b'Indicates whether a facility has been closed by the regulator'),
        ),
    ]
