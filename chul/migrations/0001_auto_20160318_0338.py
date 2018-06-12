# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chul', 'set_code_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityhealthunit',
            name='number_of_chvs',
            field=models.PositiveIntegerField(default=0, help_text=b'Number of Community Health volunteers in the CHU'),
        ),
        migrations.AlterField(
            model_name='communityhealthunit',
            name='households_monitored',
            field=models.PositiveIntegerField(default=0, help_text=b'The number of house holds a CHU is in-charge of'),
        ),
    ]
