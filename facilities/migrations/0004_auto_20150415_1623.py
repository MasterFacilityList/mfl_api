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
        ('facilities', '0003_auto_20150415_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicComprehensiveService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='basiccomprehensivesevice',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='basiccomprehensivesevice',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='b_c_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='facilities.BasicComprehensiveService', null=True),
        ),
        migrations.DeleteModel(
            name='BasicComprehensiveSevice',
        ),
    ]
