# -*- coding: utf-8 -*-
from django.db import models, migrations
from facilities.models import Facility

def set_min_code_value(apps, schema_editor):
    from django.db import connection
    cursor = connection.cursor()
    sql = """
          ALTER SEQUENCE common_county_code_seq restart 100 start 100000 minvalue 100
          """
    cursor = cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_min_code_value),
    ]
