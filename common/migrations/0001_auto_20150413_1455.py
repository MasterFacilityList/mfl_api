# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', 'custom_common_sequences'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituency',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='contact',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='contacttype',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='county',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='subcounty',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
    ]
