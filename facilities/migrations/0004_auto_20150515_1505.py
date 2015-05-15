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
        ('facilities', '0003_auto_20150512_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingScale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('value', models.CharField(max_length=3)),
                ('display_text', models.TextField(help_text=b'What the user will see')),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='facilitycontact',
            name='facility',
            field=models.ForeignKey(related_name='facility_contacts', on_delete=django.db.models.deletion.PROTECT, to='facilities.Facility'),
        ),
        migrations.AlterField(
            model_name='servicerating',
            name='attitude',
            field=models.ForeignKey(related_name='attitude_ratings', to='facilities.RatingScale'),
        ),
        migrations.AlterField(
            model_name='servicerating',
            name='cleanliness',
            field=models.ForeignKey(related_name='cleanliness_rating', to='facilities.RatingScale'),
        ),
        migrations.AlterField(
            model_name='servicerating',
            name='will_return',
            field=models.ForeignKey(related_name='return_rating', to='facilities.RatingScale'),
        ),
    ]
