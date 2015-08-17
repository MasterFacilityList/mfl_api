# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150817_0630'),
        ('facilities', 'set_facility_code_sequence_min_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='location_desc',
            field=models.TextField(help_text=b'This field allows a more detailed description of the location', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='nearest_landmark',
            field=models.TextField(help_text=b'well-known physical features /structure that can be used to simplify directions to a given place. e.g town market or village ', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='plot_number',
            field=models.CharField(help_text=b'This is the same number found on the title deeds of thepiece of land on which this facility is located', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='town',
            field=models.ForeignKey(blank=True, to='common.Town', help_text=b'The town where the entity is located e.g Nakuru', null=True),
        ),
    ]
