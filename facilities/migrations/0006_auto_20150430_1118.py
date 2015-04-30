# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20150430_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulationstatus',
            name='description',
            field=models.TextField(help_text=b"A short description of the regulation state or state e.gPENDING_OPENING could be descriped as 'waiting for the license tobegin operating' ", null=True, blank=True),
        ),
    ]
