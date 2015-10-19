# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_remove_documentupload_public'),
        ('admin_offices', '0002_auto_20151009_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminoffice',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='adminoffice',
            name='sub_county',
            field=models.ForeignKey(blank=True, to='common.SubCounty', null=True),
        ),
        migrations.AlterField(
            model_name='adminoffice',
            name='county',
            field=models.ForeignKey(blank=True, to='common.County', null=True),
        ),
    ]
