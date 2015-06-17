# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_regulatorybodyuser'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='regulatorybodyuser',
            unique_together=set([('regulatory_body', 'user')]),
        ),
    ]
