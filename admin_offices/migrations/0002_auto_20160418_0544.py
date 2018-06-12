# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_offices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminoffice',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='adminoffice',
            name='is_national',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='adminoffice',
            name='phone_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
