# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='county',
            name='Province',
            field=models.ForeignKey(blank=True, to='common.Province', null=True),
        ),
    ]
