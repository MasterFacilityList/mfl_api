# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_auto_20170521_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noficiationgroup',
            name='notification',
            field=models.ForeignKey(related_name='notification_groups', to='common.Notification'),
        ),
    ]
