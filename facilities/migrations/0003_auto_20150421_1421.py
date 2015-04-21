# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150421_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'ordering': ('-updated', '-created'), 'verbose_name_plural': 'service categories'},
        ),
        migrations.AddField(
            model_name='service',
            name='abbreviation',
            field=models.CharField(help_text=b'A short form for the service e.g FANC for Focused Antenatal Care', max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='servicecategory',
            name='abbreviation',
            field=models.CharField(help_text=b'A short form of the category e.g ANC for antenatal', max_length=50, null=True, blank=True),
        ),
    ]
