# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0003_auto_20160324_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chuservicelink',
            old_name='chu',
            new_name='health_unit',
        ),
        migrations.AlterUniqueTogether(
            name='chuservicelink',
            unique_together=set([('health_unit', 'service')]),
        ),
    ]
