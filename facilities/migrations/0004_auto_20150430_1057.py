# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20150429_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulatingbody',
            name='abbreviation',
            field=models.CharField(help_text=b'A shortform of the name of the regulating body e.g NursingCouncil of Kenya could be abbreviated as NCK.', max_length=50, null=True, blank=True),
        ),
    ]
