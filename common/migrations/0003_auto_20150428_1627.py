# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150428_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituency',
            name='name',
            field=models.CharField(help_text=b'Name og the region may it be e.g Nairobi', max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='constituency',
            unique_together=set([('county', 'name')]),
        ),
    ]
