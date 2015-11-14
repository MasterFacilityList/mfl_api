# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import migrations


fname = os.path.join(
    os.path.dirname(__file__), 'create_drilldown_mat_view.sql'
)

with open(fname) as f:
    mat_view_sql = f.read()


class Migration(migrations.Migration):

    dependencies = [
        ('mfl_gis', '0001_initial', ),
    ]

    operations = [
        migrations.RunSQL(mat_view_sql)
    ]
