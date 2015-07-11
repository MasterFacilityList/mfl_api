# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAdminUnitLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('county_level', models.BooleanField(default=False, help_text=b'Indicates whether a group applies at county level')),
                ('constituency_level', models.BooleanField(default=False, help_text=b'Indicates whether a group applies at county level')),
                ('national_level', models.BooleanField(default=False, help_text=b'Indicates whether a group applies at county level')),
                ('group', models.OneToOneField(related_name='admin_level', to='auth.Group')),
            ],
        ),
    ]
