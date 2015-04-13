# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mfluser',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='usercounties',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
    ]
