# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0004_auto_20150402_1256'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rolepermissions',
            unique_together=set([('role', 'permission')]),
        ),
    ]
