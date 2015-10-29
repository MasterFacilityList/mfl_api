# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0012_auto_20151026_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicecategory',
            name='keph_level',
        ),
        migrations.AddField(
            model_name='facility',
            name='facility_catchment_population',
            field=models.IntegerField(help_text=b'The population size which the facility serves', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='service',
            name='keph_level',
            field=models.ForeignKey(blank=True, to='facilities.KephLevel', help_text=b'The KEPH level at which the service ought to be offered', null=True),
        ),
        migrations.AddField(
            model_name='servicecategory',
            name='parent',
            field=models.ForeignKey(blank=True, to='facilities.ServiceCategory', help_text=b'The parent category under which the category falls', null=True),
        ),
    ]
