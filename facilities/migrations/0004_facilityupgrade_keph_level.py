# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_remove_kephlevel_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityupgrade',
            name='keph_level',
            field=models.ForeignKey(to='facilities.KephLevel', null=True),
        ),
    ]
