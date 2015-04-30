# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20150430_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulatingbody',
            name='name',
            field=models.CharField(help_text=b'The name of the regulating body', max_length=100, unique=True, null=True, blank=True),
        ),
    ]
