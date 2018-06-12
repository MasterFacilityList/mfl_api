# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_countymapping'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CountyMapping',
        ),
    ]
