# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_offices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminofficecontact',
            name='admin_office',
            field=models.ForeignKey(related_name='contacts', to='admin_offices.AdminOffice'),
        ),
    ]
