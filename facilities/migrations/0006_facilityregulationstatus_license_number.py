# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20150427_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='license_number',
            field=models.CharField(help_text=b'The license number that the facility has been given by the regulator', max_length=100, null=True, blank=True),
        ),
    ]
