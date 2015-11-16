# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobtitle',
            options={'permissions': (('view_jobtitle', 'Can view job title'),)},
        ),
        migrations.AlterField(
            model_name='mfluser',
            name='job_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='users.JobTitle', help_text=b'The job title of the user e.g County Reproductive Health Officer', null=True),
        ),
    ]
