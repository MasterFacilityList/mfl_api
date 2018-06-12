# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20160407_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconstituency',
            name='constituency',
            field=models.ForeignKey(to='common.Constituency', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='userconstituency',
            name='user',
            field=models.ForeignKey(related_name='user_constituencies', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercontact',
            name='contact',
            field=models.ForeignKey(to='common.Contact', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='usersubcounty',
            name='user',
            field=models.ForeignKey(related_name='user_sub_counties', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
