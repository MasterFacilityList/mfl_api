# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20150427_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coverreporttemplate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='coverreporttemplate',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='inspectionreport',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='inspectionreport',
            name='updated_by',
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'ordering': ('-updated', '-created'), 'verbose_name_plural': 'facilities'},
        ),
        migrations.DeleteModel(
            name='CoverReportTemplate',
        ),
        migrations.DeleteModel(
            name='InspectionReport',
        ),
    ]
