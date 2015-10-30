# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0003_auto_20151027_1051'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='communityhealthunit',
            unique_together=set([('name', 'facility')]),
        ),
    ]
