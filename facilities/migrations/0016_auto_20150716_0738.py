# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0015_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facility',
            options={'ordering': ('-updated', '-created'), 'default_permissions': ('add', 'change', 'delete', 'view'), 'verbose_name_plural': 'facilities', 'permissions': (('view_classified_facilities', 'Can see classified facilities'), ('publish_facilities', 'Can publish facilities'), ('view_unpublished_facilities', 'Can view the un published facilities'), ('view_approved_facilities', 'Can view the un published facilities'))},
        ),
    ]
