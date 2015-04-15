# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facilitycontact',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='facilitygps',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='facilityservice',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='facilitystatus',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='facilityunit',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='geocodemethod',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='geocodesource',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='jobtitle',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='officerincharge',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='officerinchargecontact',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='owner',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='ownertype',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='regulatingbody',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='regulationstatus',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('-updated', '-created')},
        ),
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'ordering': ('-updated', '-created')},
        ),
    ]
