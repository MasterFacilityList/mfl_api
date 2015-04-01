# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('users', '0002_remove_userdetail_sub_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='sub_location',
            field=models.ForeignKey(default=1, to='common.SubLocation'),
        ),
    ]
