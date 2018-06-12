# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0031_auto_20171124_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiauthentication',
            name='server',
            field=models.CharField(default=b'https://test.hiskenya.org/dev/', max_length=255),
        ),
    ]
