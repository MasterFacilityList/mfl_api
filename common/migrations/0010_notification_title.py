# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='Default  Title', max_length=255),
            preserve_default=False,
        ),
    ]
