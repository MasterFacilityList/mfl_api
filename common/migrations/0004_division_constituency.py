# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_district_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='constituency',
            field=models.ForeignKey(blank=True, to='common.Constituency', null=True),
        ),
    ]
