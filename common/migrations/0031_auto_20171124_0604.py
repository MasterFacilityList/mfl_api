# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0030_auto_20171123_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiauthentication',
            name='server',
            field=models.CharField(default=b'http://test.hiskenya.org/dev/', max_length=255),
        ),
    ]
