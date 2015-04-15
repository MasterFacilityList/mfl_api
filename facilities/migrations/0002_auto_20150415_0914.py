# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import common.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityRatingScale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(related_name='facility_rating_scales', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility')),
            ],
        ),
        migrations.CreateModel(
            name='FacilityServiceRatingScale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility_service', models.ForeignKey(related_name='facility_service_scale', on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityService')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('rating_code', models.CharField(help_text=b'A code representing  a rate e.g 1, Likely etc', max_length=30)),
                ('description', models.TextField(help_text=b'An explanation of how the rating code is used', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RatingScale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(help_text=b'The name of the rating scale e.g likert RatingScale', unique=True, max_length=100)),
                ('description', models.TextField(help_text=b'A summary of the type of rating scale. E.g What it is. ')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserFacilityRating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('comment', models.TextField(help_text=b'Reason for picking that rate.', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(related_name='facility_rating', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility')),
                ('rating', models.ForeignKey(to='facilities.Rating', on_delete=django.db.models.deletion.PROTECT)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user_facility_rating', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFacitlityServiceRating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('comment', models.TextField(help_text=b'Reason for picking that rate.', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility_service', models.ForeignKey(to='facilities.FacilityService', on_delete=django.db.models.deletion.PROTECT)),
                ('rating', models.ForeignKey(to='facilities.Rating', on_delete=django.db.models.deletion.PROTECT)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user_service_rating', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='scale',
            field=models.ForeignKey(to='facilities.RatingScale', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='rating',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityserviceratingscale',
            name='scale',
            field=models.ForeignKey(related_name='facility_service_using_scale', on_delete=django.db.models.deletion.PROTECT, to='facilities.RatingScale'),
        ),
        migrations.AddField(
            model_name='facilityserviceratingscale',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityratingscale',
            name='scale',
            field=models.ForeignKey(related_name='facilities_using_scale', on_delete=django.db.models.deletion.PROTECT, to='facilities.RatingScale'),
        ),
        migrations.AddField(
            model_name='facilityratingscale',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userfacitlityservicerating',
            unique_together=set([('facility_service', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='userfacilityrating',
            unique_together=set([('facility', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('scale', 'rating_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='facilityserviceratingscale',
            unique_together=set([('facility_service', 'scale')]),
        ),
        migrations.AlterUniqueTogether(
            name='facilityratingscale',
            unique_together=set([('facility', 'scale')]),
        ),
    ]
