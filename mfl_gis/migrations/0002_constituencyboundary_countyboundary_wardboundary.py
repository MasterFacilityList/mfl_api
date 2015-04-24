# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import common.models.base
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mfl_gis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConstituencyBoundary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(max_length=100)),
                ('polygons', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('constituency', models.OneToOneField(to='common.Constituency')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
                'verbose_name_plural': 'constituency boundaries',
            },
        ),
        migrations.CreateModel(
            name='CountyBoundary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(max_length=100)),
                ('polygons', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('county', models.OneToOneField(to='common.County')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
                'verbose_name_plural': 'county boundaries',
            },
        ),
        migrations.CreateModel(
            name='WardBoundary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(max_length=100)),
                ('polygons', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('ward', models.OneToOneField(to='common.Ward')),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
                'verbose_name_plural': 'ward boundaries',
            },
        ),
    ]
