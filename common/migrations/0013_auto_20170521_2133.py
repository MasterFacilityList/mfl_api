# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import common.models.base
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('common', '0012_auto_20160525_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoficiationGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='notification',
            name='group',
        ),
        migrations.AddField(
            model_name='noficiationgroup',
            name='notification',
            field=models.ForeignKey(to='common.Notification'),
        ),
        migrations.AddField(
            model_name='noficiationgroup',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
    ]
