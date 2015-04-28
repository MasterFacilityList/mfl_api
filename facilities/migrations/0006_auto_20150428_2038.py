# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20150428_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='location_desc',
            field=models.TextField(help_text=b'This field allows a more detailed description of how tolocate the facility e.g Joy medical clinic is in Jubilee Plaza7th Floor', null=True, blank=True),
        ),
    ]
