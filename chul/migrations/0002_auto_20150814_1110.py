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
            options={'ordering': ('-updated', '-created'), 'default_permissions': ('add', 'change', 'delete', 'view'), 'verbose_name_plural': 'approval_statuses'},
        ),
        migrations.AlterModelOptions(
            name='communityhealthunitapproval',
            options={'ordering': ('-updated', '-created'), 'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
    ]
