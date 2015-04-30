# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0008_auto_20150430_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobtitle',
            name='name',
            field=models.CharField(help_text=b'A short name for the job title', max_length=100, null=True, blank=True),
        ),
    ]
