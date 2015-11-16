# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151111_1043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobtitle',
            options={'ordering': ('-created',), 'permissions': (('view_jobtitle', 'Can view job title'),)},
        ),
    ]
