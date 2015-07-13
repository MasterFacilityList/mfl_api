# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mfluser',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'permissions': (('county_group_marker', 'A marker permission for county level groups'),)},
        ),
    ]
