# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_auto_20160520_1033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-created',)},
        ),
    ]
