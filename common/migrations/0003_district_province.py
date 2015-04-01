# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150401_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(blank=True, to='common.Province', null=True),
        ),
    ]
