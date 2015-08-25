# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150824_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='group',
            field=models.ForeignKey(related_name='options', on_delete=django.db.models.deletion.PROTECT, to='facilities.OptionGroup', help_text=b'The option group where the option lies'),
        ),
    ]
