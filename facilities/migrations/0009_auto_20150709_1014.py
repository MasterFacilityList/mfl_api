# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0008_facilityapproval_is_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='regulationstatus',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='regulationstatus',
            name='regulated',
            field=models.BooleanField(default=False),
        ),
    ]
