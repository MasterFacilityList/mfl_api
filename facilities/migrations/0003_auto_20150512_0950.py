# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150511_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityservice',
            name='facility',
            field=models.ForeignKey(related_name='facility_services', to='facilities.Facility'),
        ),
    ]
