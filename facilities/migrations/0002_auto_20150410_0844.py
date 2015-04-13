# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityGPS',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(max_length=128)),
                ('updated_by', models.CharField(max_length=128)),
                ('latitude', models.CharField(help_text=b'How far north or south a facility is from the equator', max_length=255)),
                ('longitude', models.CharField(help_text=b'How far east or west one a facility is from the Greenwich Meridian', max_length=255)),
                ('is_classified', models.BooleanField(default=False, help_text=b'Should the facility be visible to the public?')),
                ('facility', models.OneToOneField(to='facilities.Facility')),
                ('methof', models.ForeignKey(help_text=b'Method used to obtain the geo codes. e.g taken with GPS device', to='facilities.GeoCodeMethod')),
                ('source_of_geo', models.ForeignKey(help_text=b'where the geo code came from', to='facilities.GeoCodeSource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='facitlitygps',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='facitlitygps',
            name='methof',
        ),
        migrations.RemoveField(
            model_name='facitlitygps',
            name='source_of_geo',
        ),
        migrations.DeleteModel(
            name='FacitlityGPS',
        ),
    ]
