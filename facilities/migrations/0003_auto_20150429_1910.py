# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150429_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitystatus',
            name='name',
            field=models.CharField(help_text=b'A short name respresenting the operanation status e.g OPERATIONAL', max_length=100, unique=True, null=True, blank=True),
        ),
    ]
