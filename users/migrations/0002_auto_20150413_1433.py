# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mfluser',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.County', null=True),
        ),
        migrations.AlterField(
            model_name='usercounties',
            name='county',
            field=models.ForeignKey(to='common.County', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='usercounties',
            name='user',
            field=models.ForeignKey(related_name='user_counties', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
