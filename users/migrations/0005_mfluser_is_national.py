# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150402_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='mfluser',
            name='is_national',
            field=models.BooleanField(default=False),
        ),
    ]
