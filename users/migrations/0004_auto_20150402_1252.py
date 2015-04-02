# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150402_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetail',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='county',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserDetail',
        ),
    ]
