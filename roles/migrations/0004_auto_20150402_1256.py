# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0003_auto_20150402_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolepermissions',
            name='permission',
            field=models.ForeignKey(to='roles.Permission'),
        ),
    ]
