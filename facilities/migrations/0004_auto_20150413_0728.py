# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20150412_1756'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OwnerTypes',
            new_name='OwnerType',
        ),
    ]
