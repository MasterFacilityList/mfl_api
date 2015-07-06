# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150629_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='town',
            name='ward',
            field=models.ForeignKey(blank=True, to='common.Ward', help_text=b'The ward where the town is located', null=True),
        ),
    ]
