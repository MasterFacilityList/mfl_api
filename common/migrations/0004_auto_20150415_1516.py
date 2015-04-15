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
        ('common', '0003_auto_20150415_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCounty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('county', models.ForeignKey(to='common.County', on_delete=django.db.models.deletion.PROTECT)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user_counties', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'user_counties',
            },
        ),
        migrations.RemoveField(
            model_name='usercounties',
            name='county',
        ),
        migrations.RemoveField(
            model_name='usercounties',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='usercounties',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='usercounties',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserCounties',
        ),
    ]
