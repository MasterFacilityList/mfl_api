# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151027_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'A short name for the job title', unique=True, max_length=100)),
                ('abbreviation', models.CharField(help_text=b'The short name for the title', max_length=100, null=True, blank=True)),
                ('description', models.TextField(help_text=b'A short summary of the job title', null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='mfluser',
            name='job_title',
            field=models.ForeignKey(blank=True, to='users.JobTitle', help_text=b'The job title of the user e.g County Reproductive Health Officer', null=True),
        ),
    ]
