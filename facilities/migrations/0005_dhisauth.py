# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_apiauthentication'),
        ('facilities', '0004_auto_20170905_0408'),
    ]

    operations = [
        migrations.CreateModel(
            name='DhisAuth',
            fields=[
                ('apiauthentication_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='common.ApiAuthentication')),
                ('oauth2_token_variable_name', models.CharField(default=b'api_oauth2_token', max_length=255)),
                ('type', models.CharField(default=b'DHIS2', max_length=255)),
            ],
            bases=('common.apiauthentication',),
        ),
    ]
