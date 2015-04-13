# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subcounty',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subcounty',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='county',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='county',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contacttype',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contacttype',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.ContactType', help_text=b'The type of contact that the given contact is e.g email or phone number'),
        ),
        migrations.AddField(
            model_name='contact',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contact',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='constituency',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.County', help_text=b'Name of the county where the constituency is located'),
        ),
        migrations.AddField(
            model_name='constituency',
            name='created_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='constituency',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.get_default_system_user, to=settings.AUTH_USER_MODEL),
        ),
    ]
