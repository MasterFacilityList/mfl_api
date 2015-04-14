# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import common.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0003_auto_20150414_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(help_text=b'A short summary of the facility unit.')),
                ('is_approved', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='facility',
            name='parent',
            field=models.ForeignKey(default='1a049a8a-6e1f-4427-9098-a779cf9f63fa', to='facilities.Facility', help_text=b'Indicates the umbrella facility of a facility'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='facilityunit',
            name='facility',
            field=models.ForeignKey(to='facilities.Facility', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='facilityunit',
            name='regulating_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.RegulatingBody', null=True),
        ),
        migrations.AddField(
            model_name='facilityunit',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
    ]
