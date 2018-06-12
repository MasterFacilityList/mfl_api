# -*- coding: utf-8 -*-
from django.db import models, migrations
from facilities.models import Facility

def set_min_code_value(apps, schema_editor):
    from django.db import connection
    cursor = connection.cursor()
    sql = """
          ALTER SEQUENCE chul_communityhealthunit_code_seq restart 700000start 700000 minvalue 700000;
          """
    cursor = cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_min_code_value),
    ]
