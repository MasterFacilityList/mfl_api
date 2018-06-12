# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0029_auto_20171023_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiauthentication',
            name='client_id',
            field=models.CharField(default=b'101', max_length=255),
        ),
        migrations.AlterField(
            model_name='apiauthentication',
            name='client_secret',
            field=models.CharField(default=b'873079d99-95b4-46f5-8369-9f23a3dd877', max_length=255),
        ),
        migrations.AlterField(
            model_name='apiauthentication',
            name='server',
            field=models.CharField(default=b'http://test.hiskenya.org/dev', max_length=255),
        ),
    ]
