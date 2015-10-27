# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0002_auto_20151027_1039'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='communityhealthworker',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='communityhealthworker',
            name='id_number',
        ),
    ]
