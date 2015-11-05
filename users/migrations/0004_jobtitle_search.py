# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151105_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtitle',
            name='search',
            field=models.TextField(help_text=b'A dummy field to enable search on the model through a filter', null=True, blank=True),
        ),
    ]
