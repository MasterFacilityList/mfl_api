# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20151114_1105'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='errorqueue',
            unique_together=set([('object_pk', 'app_label', 'model_name')]),
        ),
    ]
