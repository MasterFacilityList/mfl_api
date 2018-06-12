# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0028_facilitymapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiauthentication',
            name='client_id',
            field=models.CharField(default=b'102', max_length=255),
        ),
        migrations.AlterField(
            model_name='apiauthentication',
            name='client_secret',
            field=models.CharField(default=b'4b04e4e72-6542-3f78-f76b-37a3de0bdec', max_length=255),
        ),
    ]
