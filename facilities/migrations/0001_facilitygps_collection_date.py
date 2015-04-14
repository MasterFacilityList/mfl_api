# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'custom_facility_sequences'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitygps',
            name='collection_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 12, 21, 36, 782501, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
