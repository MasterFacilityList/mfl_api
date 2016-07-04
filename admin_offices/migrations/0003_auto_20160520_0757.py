# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_offices', '0002_auto_20160418_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminoffice',
            name='name',
            field=models.CharField(default='None', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adminoffice',
            name='constituency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.Constituency', null=True),
        ),
        migrations.AlterField(
            model_name='adminoffice',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.County', null=True),
        ),
        migrations.AlterField(
            model_name='adminoffice',
            name='first_name',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adminoffice',
            name='job_title',
            field=models.ForeignKey(to='users.JobTitle', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='adminoffice',
            name='last_name',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adminoffice',
            name='sub_county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='common.SubCounty', null=True),
        ),
        migrations.AlterField(
            model_name='adminofficecontact',
            name='admin_office',
            field=models.ForeignKey(related_name='contacts', on_delete=django.db.models.deletion.PROTECT, to='admin_offices.AdminOffice'),
        ),
    ]
