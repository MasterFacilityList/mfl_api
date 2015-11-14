# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_errorqueue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorqueue',
            name='error_type',
            field=models.CharField(max_length=100, choices=[(b'SEARCH_INDEXING_ERROR', b'An error that occurred during search indexing'), (b'SEND_EMAIL_ERROR', b'An error that occurs when sending a user email')]),
        ),
    ]
