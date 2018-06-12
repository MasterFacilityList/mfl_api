# -*- coding: utf-8 -*-
from django.db import models, migrations
from facilities.models import Facility

def set_min_code_value(apps, schema_editor):
    from django.db import connection
    cursor = connection.cursor()
    sql = """
          ALTER SEQUENCE facilities_facility_code_seq restart 100000 start 100000 minvalue 100000;
          ALTER SEQUENCE facilities_owner_code_seq restart 1000 start 1000 minvalue 1000;
          ALTER SEQUENCE facilities_service_code_seq restart 1000 start 1000 minvalue 1000;
          """
    cursor = cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_min_code_value),
    ]
