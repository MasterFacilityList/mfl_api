# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20151029_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacttype',
            name='name',
            field=models.CharField(help_text=b'A short name, preferably 6 characters long, representing a certain type of contact e.g EMAIL', unique=True, max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='usercontact',
            unique_together=set([('user', 'contact')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercounty',
            unique_together=set([('user', 'county')]),
        ),
    ]
