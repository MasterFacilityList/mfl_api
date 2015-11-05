# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0015_auto_20151029_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobtitle',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='jobtitle',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='officer',
            name='job_title',
            field=models.ForeignKey(to='users.JobTitle', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='parent',
            field=models.ForeignKey(related_name='sub_categories', blank=True, to='facilities.ServiceCategory', help_text=b'The parent category under which the category falls', null=True),
        ),
        migrations.DeleteModel(
            name='JobTitle',
        ),
    ]
