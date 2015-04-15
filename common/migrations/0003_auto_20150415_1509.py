# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150415_0714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constituency',
            options={'verbose_name_plural': 'constituencies'},
        ),
        migrations.AlterModelOptions(
            name='county',
            options={'verbose_name_plural': 'counties'},
        ),
        migrations.AlterModelOptions(
            name='physicaladdress',
            options={'verbose_name_plural': 'physical addresses'},
        ),
        migrations.AlterModelOptions(
            name='usercounties',
            options={'verbose_name_plural': 'user_counties'},
        ),
    ]
