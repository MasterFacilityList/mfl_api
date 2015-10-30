# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0013_auto_20151027_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regulatorsync',
            name='mfl_code',
        ),
        migrations.AddField(
            model_name='regulatorsync',
            name='regulatory_body',
            field=models.ForeignKey(blank=True, to='facilities.RegulatingBody', help_text=b'The regulatory body the record came from', null=True),
        ),
        migrations.AlterField(
            model_name='regulatorsync',
            name='name',
            field=models.CharField(help_text=b'The official name of the facility', max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='facilitytype',
            unique_together=set([('name',)]),
        ),
    ]
