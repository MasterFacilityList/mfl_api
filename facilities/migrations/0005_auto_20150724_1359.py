# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_facilityupgrade_keph_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='official_name',
            field=models.CharField(help_text=b'The official name of the facility', max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='name',
            field=models.CharField(help_text=b'This is the unique name of the facility', unique=True, max_length=100),
        ),
    ]
