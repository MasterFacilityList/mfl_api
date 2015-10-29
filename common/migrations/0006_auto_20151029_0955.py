# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20151029_0934'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userconstituency',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='usercontact',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='usercounty',
            unique_together=set([]),
        ),
    ]
