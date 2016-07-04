# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0004_auto_20160329_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='churating',
            name='chu',
            field=models.ForeignKey(related_name='chu_ratings', on_delete=django.db.models.deletion.PROTECT, to='chul.CommunityHealthUnit'),
        ),
        migrations.AlterField(
            model_name='communityhealthunit',
            name='status',
            field=models.ForeignKey(to='chul.Status', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='communityhealthworker',
            name='health_unit',
            field=models.ForeignKey(related_name='health_unit_workers', on_delete=django.db.models.deletion.PROTECT, to='chul.CommunityHealthUnit', help_text=b'The health unit the worker is in-charge of'),
        ),
        migrations.AlterField(
            model_name='communityhealthworkercontact',
            name='contact',
            field=models.ForeignKey(to='common.Contact', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='communityhealthworkercontact',
            name='health_worker',
            field=models.ForeignKey(to='chul.CommunityHealthWorker', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
