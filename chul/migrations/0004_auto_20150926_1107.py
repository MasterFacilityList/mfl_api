# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0003_chuupdatebuffer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chuupdatebuffer',
            old_name='is_cancelled',
            new_name='is_approved',
        ),
    ]
