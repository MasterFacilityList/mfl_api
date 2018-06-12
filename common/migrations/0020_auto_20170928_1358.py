# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0019_auto_20170928_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countymapping',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
        ),
        migrations.AlterField(
            model_name='countymapping',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
        ),
    ]
