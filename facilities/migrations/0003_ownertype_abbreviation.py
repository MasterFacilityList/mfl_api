# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150806_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownertype',
            name='abbreviation',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
