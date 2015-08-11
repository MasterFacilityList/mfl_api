# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_subcounty'),
        ('facilities', '0001_auto_20150810_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='sub_county',
            field=models.ForeignKey(blank=True, to='common.SubCounty', help_text=b'The sub county in which the facility has been assigned', null=True),
        ),
    ]
