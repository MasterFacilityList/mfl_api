# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userconstituency',
            options={'verbose_name_plural': 'user constituencies'},
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('contact', 'contact_type')]),
        ),
    ]
