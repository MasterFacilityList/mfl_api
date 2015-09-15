# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_facilitydepartment_regulatory_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitydepartment',
            name='regulatory_body',
            field=models.ForeignKey(to='facilities.RegulatingBody'),
        ),
    ]
