# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_auto_20150730_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitytype',
            name='abbreviation',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='abbreviation',
            field=models.CharField(help_text=b'The short name for the title', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='regulatingbody',
            name='default_status',
            field=models.ForeignKey(blank=True, to='facilities.RegulationStatus', help_text=b'The default status for the facilities regulated by the particular regulator', null=True),
        ),
    ]
