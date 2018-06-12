# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facilityexportexcelmaterialview',
            options={'ordering': ('-created',), 'managed': False},
        ),
    ]
