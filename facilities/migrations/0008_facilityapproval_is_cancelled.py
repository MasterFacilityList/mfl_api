# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_auto_20150629_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityapproval',
            name='is_cancelled',
            field=models.BooleanField(default=False, help_text=b'Cancel a facility approval'),
        ),
    ]
