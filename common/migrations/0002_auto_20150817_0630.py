# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacttype',
            name='name',
            field=models.CharField(help_text=b'A short name, preferrably 6 characters long, representing a certain type of contact e.g EMAIL', unique=True, max_length=100),
        ),
    ]
