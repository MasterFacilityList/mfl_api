# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chul', 'set_code_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityhealthunit',
            name='date_established',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='communityhealthunit',
            name='date_operational',
            field=models.DateField(null=True, blank=True),
        ),
    ]
