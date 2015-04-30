# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0006_auto_20150430_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulationstatus',
            name='name',
            field=models.CharField(help_text=b'A short unique name representing a state/stage of regulation e.g. PENDING_OPENING ', max_length=100, unique=True, null=True, blank=True),
        ),
    ]
