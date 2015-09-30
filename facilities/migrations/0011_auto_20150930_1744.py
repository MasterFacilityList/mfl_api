# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0010_regulatorsync'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='facilitytype',
            unique_together=set([('name',)]),
        ),
    ]
