# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', 'set_code_sequence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='communityhealthunitcontact',
            options={'permissions': (('view_communityhealthunitcontact', 'Can view community health_unit contact'),)},
        ),
        migrations.AlterField(
            model_name='communityhealthworker',
            name='health_unit',
            field=models.ForeignKey(related_name='health_unit_workers', to='chul.CommunityHealthUnit', help_text=b'The health unit the worker is in-charge of'),
        ),
    ]
