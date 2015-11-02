# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0014_auto_20151029_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='regulatorsync',
            name='mfl_code',
            field=models.PositiveIntegerField(help_text=b'The assigned MFL code', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='regulatorsync',
            name='regulatory_body',
            field=models.ForeignKey(help_text=b'The regulatory body the record came from', to='facilities.RegulatingBody'),
        ),
    ]
