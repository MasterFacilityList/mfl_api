# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_offices', '0004_remove_adminoffice_job_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminoffice',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='adminoffice',
            name='last_name',
        ),
        migrations.AddField(
            model_name='adminoffice',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='adminoffice',
            name='code',
            field=common.fields.SequenceField(help_text=b'A unique number to identify the admin office.', unique=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='adminoffice',
            name='old_code',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
