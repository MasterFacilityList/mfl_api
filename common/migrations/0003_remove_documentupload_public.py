# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_documentupload_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentupload',
            name='public',
        ),
    ]
