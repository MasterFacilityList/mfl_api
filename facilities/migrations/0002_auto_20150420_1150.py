# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.models.base
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(help_text=b'A short name for the practioner type e.g DENTIST', unique=True, max_length=50)),
                ('description', models.TextField(help_text=b'A description of the practitioner type', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Practitioner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(max_length=150)),
                ('registration_number', models.CharField(help_text=b'The registration_number of the practitioner.', unique=True, max_length=20)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PractitionerContact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('contact', models.ForeignKey(to='common.Contact')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('practitioner', models.ForeignKey(to='facilities.Practitioner')),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PractitionerFacility',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('is_owner', models.BooleanField(default=False, help_text=b'Does the practitioner own the facility?')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(to='facilities.Facility')),
                ('practitioner', models.ForeignKey(to='facilities.Practitioner')),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PractitionerQualification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('practitioner', models.ForeignKey(to='facilities.Practitioner')),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(help_text=b'A name for the Qualification e.ff MBChB(Kampla) 2011', unique=True, max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(help_text=b'A short name for the specilization e.g Endodontics', max_length=50)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('practice_type', models.ForeignKey(to='facilities.PracticeType')),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='practitionerqualification',
            name='qualification',
            field=models.ForeignKey(to='facilities.Qualification'),
        ),
        migrations.AddField(
            model_name='practitionerqualification',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='contacts',
            field=models.ManyToManyField(help_text=b'Practitioner contacts emails, phone numbers etc.', to='common.Contact', through='facilities.PractitionerContact'),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='facilities',
            field=models.ManyToManyField(to='facilities.Facility', through='facilities.PractitionerFacility'),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='qualifications',
            field=models.ManyToManyField(help_text=b'Practitioner qualifications', to='facilities.Qualification', through='facilities.PractitionerQualification'),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='speciality',
            field=models.ForeignKey(to='facilities.Speciality'),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='practitioner',
            name='ward',
            field=models.ForeignKey(blank=True, to='common.Ward', help_text=b'The ward where the practitioner comes from.', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='speciality',
            unique_together=set([('name', 'practice_type')]),
        ),
    ]
