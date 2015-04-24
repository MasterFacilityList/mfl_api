# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_auto_20150422_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='abbreviation',
            field=models.CharField(help_text=b'Short form of the name of the owner e.g Ministry of health could be shortened as MOH', max_length=30, null=True, blank=True),
        ),
    ]
