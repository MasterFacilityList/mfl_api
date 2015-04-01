# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_division_constituency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]
