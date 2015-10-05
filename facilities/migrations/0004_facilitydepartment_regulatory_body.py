# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitydepartment',
            name='regulatory_body',
            field=models.ForeignKey(blank=True, to='facilities.RegulatingBody', null=True),
        ),
    ]
