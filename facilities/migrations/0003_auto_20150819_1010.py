# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150818_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facility',
            options={'ordering': ('-updated', '-created'), 'default_permissions': ('add', 'change', 'delete', 'view'), 'verbose_name_plural': 'facilities', 'permissions': (('view_classified_facilities', 'Can see classified facilities'), ('view_closed_facilities', 'Can see closed facilities'), ('publish_facilities', 'Can publish facilities'), ('view_unpublished_facilities', 'Can see the un published facilities'), ('view_unapproved_facilities', 'Can see the unapproved facilities'), ('view_all_facility_fields', 'Can see the all information on a facilities'))},
        ),
        migrations.AddField(
            model_name='facility',
            name='closed_date',
            field=models.DateTimeField(help_text=b'Date the facility was closed', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='closing_reason',
            field=models.TextField(help_text=b'Reason for closing the facility', null=True, blank=True),
        ),
    ]
