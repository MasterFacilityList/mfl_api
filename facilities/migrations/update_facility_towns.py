# -*- coding: utf-8 -*-
from django.db import models, migrations
from facilities.models import Facility


def update_facility_names(apps, schema_editor):
    for facility in Facility.everything.all():
        if facility.town:
            try:
                facility.town_name = facility.town.name
                facility.save(allow_save=True)
            except:
                if not facility.name:
                    facility.name = facility.official_name
                    facility.town_name = facility.town.name
                    facility.save(allow_save=True)


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20160407_0910'),
    ]

    operations = [
        migrations.RunPython(update_facility_names),
    ]
