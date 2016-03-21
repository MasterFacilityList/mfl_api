# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20151116_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='ward',
            name='sub_county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.SubCounty', help_text=b'The sub-county where the ward is located', null=True),
        ),
    ]
