# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0010_auto_20150430_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='name',
            field=models.CharField(help_text=b'the name of the officer in-charge e.g Roselyne Wiyanga ', max_length=255, null=True, blank=True),
        ),
    ]
