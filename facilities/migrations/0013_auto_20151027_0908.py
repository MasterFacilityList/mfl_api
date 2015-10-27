# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0012_auto_20151027_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='has_options',
            field=models.BooleanField(default=False),
        ),
    ]
