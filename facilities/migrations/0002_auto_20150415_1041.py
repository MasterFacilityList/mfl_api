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
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFacilityServiceRating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('comment', models.TextField(help_text=b'Reason for picking that rate.', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility_service', models.ForeignKey(to='facilities.FacilityService', on_delete=django.db.models.deletion.PROTECT)),
                ('rating', models.ForeignKey(to='facilities.Rating', on_delete=django.db.models.deletion.PROTECT)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user_service_rating', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userfacitlityservicerating',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='userfacitlityservicerating',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='userfacitlityservicerating',
            name='facility_service',
        ),
        migrations.RemoveField(
            model_name='userfacitlityservicerating',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='userfacitlityservicerating',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='userfacitlityservicerating',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserFacitlityServiceRating',
        ),
        migrations.AlterUniqueTogether(
            name='userfacilityservicerating',
            unique_together=set([('facility_service', 'user')]),
        ),
    ]
