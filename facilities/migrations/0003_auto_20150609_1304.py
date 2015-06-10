# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_remove_facilitytype_suceedding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='open_whole_week',
        ),
        migrations.AddField(
            model_name='facility',
            name='open_public_holidays',
            field=models.BooleanField(default=False, help_text=b'Is the facility open on public holidays?'),
        ),
        migrations.AddField(
            model_name='facility',
            name='open_weekends',
            field=models.BooleanField(default=False, help_text=b'Is the facility_open during weekends?'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='open_whole_day',
            field=models.BooleanField(default=False, help_text=b'Does the facility operate 24 hours a day'),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ForeignKey(related_name='category_services', to='facilities.ServiceCategory', help_text=b'The classification that the service lies in.'),
        ),
    ]
