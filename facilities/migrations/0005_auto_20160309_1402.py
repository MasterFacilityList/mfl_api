# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20160204_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilityapproval',
            name='comment',
            field=models.TextField(null=True, blank=True),
        ),
    ]
