# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20150827_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityupdates',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
