# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_remove_documentupload_public'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userconstituency',
            unique_together=set([('user', 'constituency')]),
        ),
    ]
