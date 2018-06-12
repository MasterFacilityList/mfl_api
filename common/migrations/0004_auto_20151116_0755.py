# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20151114_1147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='errorqueue',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='errorqueue',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
