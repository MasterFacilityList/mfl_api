# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150420_1150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='practitionerfacility',
            options={'verbose_name_plural': 'practitioner_facilities'},
        ),
        migrations.AlterModelOptions(
            name='speciality',
            options={'verbose_name_plural': 'spcialities'},
        ),
    ]
