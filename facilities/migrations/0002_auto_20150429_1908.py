# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='regulatingbody',
            name='regulation_function',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='regulatingbody',
            name='regulation_verb',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='facilitystatus',
            name='description',
            field=models.TextField(help_text=b'A short explanation of what the status entails.', null=True, blank=True),
        ),
    ]
