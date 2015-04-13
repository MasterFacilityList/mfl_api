# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', 'custom_common_sequences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituency',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.County', help_text=b'Name of the county where the constituency is located'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='contact_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.ContactType', help_text=b'The type of contact that the given contact is e.g email or phone number'),
        ),
        migrations.AlterField(
            model_name='subcounty',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.County', help_text=b'The county where the sub county is located.'),
        ),
    ]
