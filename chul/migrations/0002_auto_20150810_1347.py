# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvalstatus',
            options={'verbose_name_plural': 'approval_statuses'},
        ),
        migrations.AlterModelOptions(
            name='communityhealthunitapproval',
            options={},
        ),
        migrations.AlterModelOptions(
            name='communityhealthworker',
            options={},
        ),
        migrations.AlterModelOptions(
            name='communityhealthworkerapproval',
            options={},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'statuses'},
        ),
    ]
