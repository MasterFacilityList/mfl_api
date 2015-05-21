# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20150518_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitytype',
            name='preceding',
            field=models.ForeignKey(related_name='preceding_type', blank=True, to='facilities.FacilityType', help_text=b'The facility type that comes before this type', null=True),
        ),
    ]
