# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_auto_20150518_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratingscale',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ratingscale',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='servicerating',
            name='attitude',
        ),
        migrations.RemoveField(
            model_name='servicerating',
            name='cleanliness',
        ),
        migrations.RemoveField(
            model_name='servicerating',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='servicerating',
            name='facility_service',
        ),
        migrations.RemoveField(
            model_name='servicerating',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='servicerating',
            name='will_return',
        ),
        migrations.AddField(
            model_name='facilityservicerating',
            name='comment',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='RatingScale',
        ),
        migrations.DeleteModel(
            name='ServiceRating',
        ),
    ]
