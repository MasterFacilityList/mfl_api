# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='contacttype',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='physicaladdress',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='town',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='usercontact',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='usercounties',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='userresidence',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.RemoveField(
            model_name='usercounties',
            name='is_active',
        ),
    ]
