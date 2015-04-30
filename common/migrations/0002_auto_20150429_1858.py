# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='town',
            name='name',
            field=models.CharField(help_text=b'Name of the town', max_length=100, unique=True, null=True, blank=True),
        ),
    ]
