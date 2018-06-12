# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_facilitytype_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officercontact',
            name='officer',
            field=models.ForeignKey(related_name='officer_contacts', on_delete=django.db.models.deletion.PROTECT, to='facilities.Officer', help_text=b'The is the officer in charge'),
        ),
    ]
