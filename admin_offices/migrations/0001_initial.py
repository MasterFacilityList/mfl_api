# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import common.models.base
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import mfl_gis.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20160407_1007'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20151111_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminOffice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('constituency', models.ForeignKey(blank=True, to='common.Constituency', null=True)),
                ('county', models.ForeignKey(blank=True, to='common.County', null=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('job_title', models.ForeignKey(to='users.JobTitle')),
                ('sub_county', models.ForeignKey(blank=True, to='common.SubCounty', null=True)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
            },
            bases=(mfl_gis.models.CoordinatesValidatorMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AdminOfficeContact',
            fields=[
                ('contact_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='common.Contact')),
                ('admin_office', models.ForeignKey(related_name='contacts', to='admin_offices.AdminOffice')),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
            },
            bases=('common.contact',),
        ),
    ]
