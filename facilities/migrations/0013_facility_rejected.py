# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0012_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
