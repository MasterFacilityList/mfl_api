# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_auto_20150819_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='group',
            field=models.ForeignKey(related_name='options', to='facilities.OptionGroup', help_text=b'The option group where the option lies'),
        ),
    ]
