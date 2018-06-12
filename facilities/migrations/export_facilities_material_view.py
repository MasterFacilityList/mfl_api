# -*- coding: utf-8 -*-
import os
from django.db import models, migrations
from facilities.models import Facility

with open(os.path.dirname(__file__)+'/mat_view.sql') as f:
   mat_view_sql = f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('facilities', 'set_facility_code_sequence_min_value'),
    ]

    operations = [
        migrations.RunSQL(mat_view_sql),
    ]
