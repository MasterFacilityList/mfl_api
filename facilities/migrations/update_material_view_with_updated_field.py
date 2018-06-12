# -*- coding: utf-8 -*-
import os
from django.db import models, migrations
from facilities.models import Facility

with open(os.path.dirname(__file__)+'/facility_material_view_with_updated.sql') as f:
   mat_view_sql = f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_facilityunit_registration_number'),
    ]

    operations = [
        migrations.RunSQL(mat_view_sql),
    ]
