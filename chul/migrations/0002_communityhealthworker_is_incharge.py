# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityhealthworker',
            name='is_incharge',
            field=models.BooleanField(default=False),
        ),
    ]
