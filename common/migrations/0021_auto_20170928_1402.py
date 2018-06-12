# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0020_auto_20170928_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countymapping',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='countymapping',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
