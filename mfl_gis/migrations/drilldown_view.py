# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import migrations


with open(os.path.dirname(__file__)+'/mat_view.sql') as f:
    mat_view_sql = f.read()


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', '0001_initial', ),
    ]

    operations = [
        migrations.RunSQL(mat_view_sql)
    ]
