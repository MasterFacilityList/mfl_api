# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20160309_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='date_established',
            field=models.DateField(default=datetime.date.today, help_text=b'The date when the facility became operational'),
        ),
        migrations.AddField(
            model_name='facility',
            name='open_normal_day',
            field=models.BooleanField(default=True, help_text=b'Is the facility open from 8 am to 5 pm'),
        ),
    ]
