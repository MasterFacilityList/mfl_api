# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_offices', '0003_auto_20160520_0757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminoffice',
            name='job_title',
        ),
    ]
