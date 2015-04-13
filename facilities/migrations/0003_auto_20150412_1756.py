# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_auto_20150410_0844'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityRegulationStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(max_length=128)),
                ('updated_by', models.CharField(max_length=128)),
                ('reason', models.TextField()),
                ('facility', models.ForeignKey(to='facilities.Facility')),
                ('regulation_status', models.ForeignKey(to='facilities.RegulationStatus')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='officerichargecontact',
            name='contact',
            field=models.ForeignKey(help_text=b'The contact of the officer incharge may it be email,  mobile number etc', to='common.Contact'),
        ),
        migrations.AlterField(
            model_name='officerichargecontact',
            name='officer',
            field=models.ForeignKey(help_text=b'The is the officer in charge', to='facilities.OfficerIncharge'),
        ),
        migrations.AlterField(
            model_name='officerincharge',
            name='registration_number',
            field=models.CharField(help_text=b'This is the licence number of the officer. e.g for a nurse use the NCK registration number.', max_length=100),
        ),
    ]
