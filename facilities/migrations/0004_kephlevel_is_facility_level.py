# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='kephlevel',
            name='is_facility_level',
            field=models.BooleanField(default=True, help_text=b'Is the KEPH level applicable to facilties'),
        ),
    ]
