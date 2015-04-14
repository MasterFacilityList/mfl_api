from __future__ import unicode_literals

import os

from django.db import migrations


SQL = open(os.path.dirname(__file__) + '/sequences.sql').read()


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial', )
    ]

    operations = [
        migrations.RunSQL(SQL)
    ]
