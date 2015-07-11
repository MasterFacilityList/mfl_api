# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_town_ward'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicaladdress',
            name='address',
        ),
        migrations.RemoveField(
            model_name='physicaladdress',
            name='postal_code',
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='location_desc',
            field=models.TextField(help_text=b'This field allows a more detailed description of the location', null=True, blank=True),
        ),
    ]
