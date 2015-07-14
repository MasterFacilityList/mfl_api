# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0013_facility_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='regulationstatus',
            name='is_default',
            field=models.BooleanField(default=False, help_text=b'The default regulation status for facilties'),
        ),
    ]
