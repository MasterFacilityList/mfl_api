# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ward',
            name='name',
            field=models.CharField(help_text=b'Name og the region may it be e.g Nairobi', max_length=100),
        ),
    ]
