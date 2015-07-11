# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0010_auto_20150709_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='location_desc',
        ),
    ]
