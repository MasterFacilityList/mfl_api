# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20150806_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='name',
            field=models.CharField(help_text=b'This is the unique name of the facility', max_length=100),
        ),
    ]
