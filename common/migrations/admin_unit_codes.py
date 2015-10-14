# -*- coding: utf-8 -*-
from django.db import models, migrations
from facilities.models import Facility

def set_min_code_value(apps, schema_editor):
    from django.db import connection
    cursor = connection.cursor()
    sql = """
          ALTER SEQUENCE common_constituency_code_seq restart 1000 start 1000 minvalue 1000;
          ALTER SEQUENCE common_county_code_seq restart 1000 start 1000 minvalue 1000;
          ALTER SEQUENCE common_subcounty_code_seq restart 1000 start 1000 minvalue 1000;
          ALTER SEQUENCE common_ward_code_seq restart 10000 start 10000 minvalue 10000;
          """
    cursor = cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_min_code_value),
    ]
