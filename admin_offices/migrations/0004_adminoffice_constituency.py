# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_remove_documentupload_public'),
        ('admin_offices', '0003_auto_20151019_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminoffice',
            name='constituency',
            field=models.ForeignKey(blank=True, to='common.Constituency', null=True),
        ),
    ]
