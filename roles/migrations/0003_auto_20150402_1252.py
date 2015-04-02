# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0002_permission_rolepermissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolepermissions',
            name='permission',
            field=models.ForeignKey(related_name='permission_roles', to='roles.Permission'),
        ),
        migrations.AlterField(
            model_name='rolepermissions',
            name='role',
            field=models.ForeignKey(related_name='role_permissions', to='roles.Role'),
        ),
    ]
