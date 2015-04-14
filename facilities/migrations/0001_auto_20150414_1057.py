# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', 'custom_common_sequences'),
        ('facilities', 'custom_sequencies'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficerInchargeContact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(max_length=128)),
                ('updated_by', models.CharField(max_length=128)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Contact', help_text=b'The contact of the officer incharge may it be email,  mobile number etc')),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.OfficerIncharge', help_text=b'The is the officer in charge')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='officerichargecontact',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='officerichargecontact',
            name='officer',
        ),
        migrations.DeleteModel(
            name='OfficerIchargeContact',
        ),
    ]
