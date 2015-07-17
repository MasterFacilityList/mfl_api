# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import common.models.base
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0001_facility_has_edits'),
    ]

    operations = [
        migrations.CreateModel(
            name='KephLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('name', models.CharField(help_text=b'The name of the KEPH e.g Level 1', max_length=30)),
                ('value', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(help_text=b'A short description of the KEPH level', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='service',
            field=models.ForeignKey(blank=True, to='facilities.Service', null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='has_options',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='selected_option',
            field=models.ForeignKey(blank=True, to='facilities.ServiceOption', null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='keph_level',
            field=models.ForeignKey(blank=True, to='facilities.KephLevel', help_text=b'The keph level of the facility', null=True),
        ),
        migrations.AddField(
            model_name='servicecategory',
            name='keph_level',
            field=models.ForeignKey(blank=True, to='facilities.KephLevel', help_text=b'The keph level at which certain services should be offered', null=True),
        ),
    ]
