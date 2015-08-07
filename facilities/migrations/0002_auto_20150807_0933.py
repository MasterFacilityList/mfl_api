# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_auto_20150730_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='registration_number',
            field=models.CharField(help_text=b'The registration number given by the regulator', max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='license_is_expired',
            field=models.BooleanField(default=False, help_text=b'A flag to indicate whether the license is valid or not'),
        ),
        migrations.AddField(
            model_name='facilitytype',
            name='code',
            field=common.fields.SequenceField(help_text=b'A sequential number allocated to each facility type', unique=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='kephlevel',
            name='code',
            field=common.fields.SequenceField(help_text=b'A sequential number allocated to each keph level', unique=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='ownertype',
            name='code',
            field=common.fields.SequenceField(help_text=b'A sequential number allocated to each owner type', unique=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='regulatingbody',
            name='code',
            field=common.fields.SequenceField(help_text=b'A sequential number allocated to each regulator', unique=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='regulationstatus',
            name='code',
            field=common.fields.SequenceField(help_text=b'A sequential number allocated to each regulation status', unique=True, editable=False, blank=True),
        ),
    ]
