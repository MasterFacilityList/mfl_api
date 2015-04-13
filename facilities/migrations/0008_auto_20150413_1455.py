# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='facilitycontact',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='facilitygps',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='facilityregulationstatus',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='facilityservice',
            name='service_active',
            field=models.BooleanField(default=True, help_text=b'Is the service still being offered or not.'),
        ),
        migrations.AddField(
            model_name='facilitystatus',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='facilitytype',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='geocodemethod',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='geocodesource',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='officerichargecontact',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='officerincharge',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='owner',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='ownertype',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='regulatingbody',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='regulationstatus',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='service',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AddField(
            model_name='servicecategory',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
        migrations.AlterField(
            model_name='facilityservice',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?'),
        ),
    ]
