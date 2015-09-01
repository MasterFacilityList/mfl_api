# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150826_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='customgroup',
            name='sub_county_level',
            field=models.BooleanField(default=False, help_text=b'Will the user be creating users below the sub county level users?'),
        ),
    ]
