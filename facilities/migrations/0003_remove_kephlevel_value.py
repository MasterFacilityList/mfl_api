# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150717_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kephlevel',
            name='value',
        ),
    ]
