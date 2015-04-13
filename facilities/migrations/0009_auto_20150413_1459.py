# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0008_auto_20150413_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='code',
            field=models.CharField(help_text=b'A sequential number allocated to each facility', unique=True, max_length=100, editable=False),
        ),
        migrations.AlterField(
            model_name='owner',
            name='code',
            field=models.CharField(help_text=b'A unique number to identify the owner.Could be up to 7 characteres long.', unique=True, max_length=100, editable=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='code',
            field=models.CharField(unique=True, max_length=100, editable=False),
        ),
    ]
