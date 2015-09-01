# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_auto_20150831_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regulatingbody',
            name='contacts',
        ),
    ]
