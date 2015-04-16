# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150415_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicecategory',
            name='keph_level_service',
            field=models.BooleanField(default=False),
        ),
    ]
