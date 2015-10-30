# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='administrator',
            field=models.BooleanField(default=False, help_text=b'Will the users in this group administrator user rights?'),
        ),
    ]
