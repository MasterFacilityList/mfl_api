# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_documentupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentupload',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
