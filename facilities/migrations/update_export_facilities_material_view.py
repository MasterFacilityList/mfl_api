# -*- coding: utf-8 -*-
import os
from django.db import models, migrations
from facilities.models import Facility

with open(os.path.dirname(__file__)+'/updated_mat_view.sql') as f:
   mat_view_sql = f.read()

class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_facilitystatus_is_public_visible'),
    ]

    operations = [
        migrations.RunSQL(mat_view_sql),
    ]
