# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='officer_in_charge',
            field=models.ForeignKey(blank=True, to='facilities.Officer', help_text=b'The officer in charge of the facility', null=True),
        ),
    ]
