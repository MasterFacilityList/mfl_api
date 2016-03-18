# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0006_auto_20160309_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitystatus',
            name='is_public_visible',
            field=models.BooleanField(default=False, help_text=b'The facilities with this status should be visible to the public'),
        ),
    ]
