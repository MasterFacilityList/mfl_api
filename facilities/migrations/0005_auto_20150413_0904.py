# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20150413_0728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facilitygps',
            old_name='methof',
            new_name='method',
        ),
        migrations.RenameField(
            model_name='facilitygps',
            old_name='source_of_geo',
            new_name='source',
        ),
        migrations.AlterField(
            model_name='facilityregulationstatus',
            name='reason',
            field=models.TextField(help_text=b'e.g Why has a facility been suspended', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Is the offered or not.'),
        ),
        migrations.AlterField(
            model_name='regulatingbody',
            name='name',
            field=models.CharField(help_text=b'The name of the regulating body', unique=True, max_length=100),
        ),
    ]
