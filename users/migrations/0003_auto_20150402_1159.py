# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('users', '0002_auto_20150402_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='mfluser',
            name='contact',
            field=models.ForeignKey(blank=True, to='common.Contact', null=True),
        ),
        migrations.AddField(
            model_name='mfluser',
            name='county',
            field=models.ForeignKey(blank=True, to='common.County', null=True),
        ),
    ]
