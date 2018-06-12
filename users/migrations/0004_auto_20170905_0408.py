# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151111_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mfluser',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='mfluser',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
