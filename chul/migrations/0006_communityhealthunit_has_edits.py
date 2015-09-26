# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0005_chuupdatebuffer_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityhealthunit',
            name='has_edits',
            field=models.BooleanField(default=False, help_text=b'Indicates that a community health unit has updates that are"        " pending approval'),
        ),
    ]
