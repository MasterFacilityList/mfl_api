# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0002_auto_20150701_0759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='communityhealthworkerapproval',
            options={},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'statuses'},
        ),
    ]
