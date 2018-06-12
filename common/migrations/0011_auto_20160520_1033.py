# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_notification_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='group',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
    ]
