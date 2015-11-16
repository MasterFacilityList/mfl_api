# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', 'drilldown_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrilldownView',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('county', models.PositiveIntegerField()),
                ('constituency', models.PositiveIntegerField()),
                ('ward', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
            options={
                'db_table': 'mfl_gis_drilldown',
                'managed': False,
            },
        ),
    ]
