# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_usersubcounty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentupload',
            name='fyl',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
