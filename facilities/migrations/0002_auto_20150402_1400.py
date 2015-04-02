# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommunityUnits',
        ),
        migrations.AlterField(
            model_name='facility',
            name='services',
            field=models.ManyToManyField(to='facilities.Service', null=True, blank=True),
        ),
    ]
