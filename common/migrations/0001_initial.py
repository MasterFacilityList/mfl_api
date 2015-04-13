# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'Name og the region may it be e.g Nairobi', unique=True, max_length=100)),
                ('code', models.CharField(help_text=b'A unique_code 4 digit number representing the region.', unique=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('contact', models.CharField(help_text=b'The actual contact of the person e.g test@mail.com, 07XXYYYZZZ', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'A short name, preferrably 6 characters long, representing acertain type of contact e.g EMAIL', unique=True, max_length=100)),
                ('description', models.TextField(help_text=b'A brief desx')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'Name og the region may it be e.g Nairobi', unique=True, max_length=100)),
                ('code', models.CharField(help_text=b'A unique_code 4 digit number representing the region.', unique=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhysicalAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('town', models.CharField(help_text=b'The town where the entity is located e.g Nakuru', max_length=100, null=True, blank=True)),
                ('postal_code', models.CharField(help_text=b'The 5 digit number for the post office address. e.g 00900', max_length=100)),
                ('address', models.CharField(help_text=b'This is the actual post office number of the entity. e.g 6790', max_length=100)),
                ('nearest_landmark', models.CharField(help_text=b'well-known physical features /structure that can be used to simplify directions to a given place. e.g town market or village ', max_length=100, null=True, blank=True)),
                ('plot_number', models.CharField(help_text=b'This is the same number found on the title deeds of thepiece of land on which this facility is located', max_length=100, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubCounty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text=b'Name og the region may it be e.g Nairobi', unique=True, max_length=100)),
                ('code', models.CharField(help_text=b'A unique_code 4 digit number representing the region.', unique=True, max_length=100)),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.County', help_text=b'The county where the sub county is located.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
