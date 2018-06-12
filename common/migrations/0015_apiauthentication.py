# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_auto_20170905_0408'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiAuthentication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(default=b'healthit', max_length=255)),
                ('password', models.CharField(default=b'hEALTHIT2017', max_length=255)),
                ('client_id', models.CharField(default=b'101', max_length=255)),
                ('client_secret', models.CharField(default=b'873079d99-95b4-46f5-8369-9f23a3dd877', max_length=255)),
                ('server', models.CharField(default=b'http://test.hiskenya.org/', max_length=255)),
                ('session_key', models.CharField(default=b'dhis2_api_12904rs', max_length=255)),
            ],
        ),
    ]
