# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0004_auto_20150926_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='chuupdatebuffer',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
