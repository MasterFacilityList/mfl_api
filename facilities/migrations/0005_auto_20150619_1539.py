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
        ('facilities', '0004_remove_facility_officer_in_charge'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityUpdates',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('facility_updates', models.TextField()),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='facility',
            name='has_edits',
            field=models.BooleanField(default=False, help_text=b'Indicates that a facility has updates that have been made'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityType', help_text=b'This depends on who owns the facility. For MOH facilities,type is the gazetted classification of the facility.For Non-MOH check under the respective owners.'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='number_of_beds',
            field=models.PositiveIntegerField(default=0, help_text=b'The number of beds that a facility has. e.g 0'),
        ),
        migrations.AddField(
            model_name='facilityupdates',
            name='facility',
            field=models.ForeignKey(related_name='updates', to='facilities.Facility'),
        ),
        migrations.AddField(
            model_name='facilityupdates',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
    ]
