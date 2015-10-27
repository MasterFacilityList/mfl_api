# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0001_auto_20151009_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityhealthunit',
            name='households_monitored',
            field=models.PositiveIntegerField(help_text=b'The number of house holds a CHU is in-charge of'),
        ),
    ]
