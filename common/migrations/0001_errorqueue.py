# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', 'admin_unit_codes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.CharField(max_length=100, null=True, blank=True)),
                ('app_label', models.CharField(max_length=100, null=True, blank=True)),
                ('model_name', models.CharField(max_length=100, null=True, blank=True)),
                ('resolved', models.BooleanField(default=False)),
                ('retries', models.IntegerField(default=0)),
                ('except_message', models.TextField(null=True, blank=True)),
                ('error_type', models.CharField(max_length=20, choices=[(b'SEARCH_INDEXING_ERROR', b'An error that occurred during search indexing'), (b'SEND_EMAIL_ERROR', b'An error that occurs when sending a user email')])),
            ],
        ),
    ]
