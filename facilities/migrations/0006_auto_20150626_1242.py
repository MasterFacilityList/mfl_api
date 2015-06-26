# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20150625_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceoption',
            name='service',
            field=models.ForeignKey(related_name='service_options', to='facilities.Service'),
        ),
    ]
