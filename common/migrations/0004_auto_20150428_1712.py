# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20150428_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituency',
            name='name',
            field=models.CharField(help_text=b'Name of the region  e.g Nairobi', max_length=100),
        ),
        migrations.AlterField(
            model_name='county',
            name='name',
            field=models.CharField(help_text=b'Name of the regions e.g Nairobi', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ward',
            name='name',
            field=models.CharField(help_text=b'Name of the region e.g Nairobi', max_length=100),
        ),
    ]
