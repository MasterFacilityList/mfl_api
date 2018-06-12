# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chul', '0002_chuservicelink'),
    ]

    operations = [
        migrations.AddField(
            model_name='chuupdatebuffer',
            name='services',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chuservicelink',
            name='chu',
            field=models.ForeignKey(related_name='services', on_delete=django.db.models.deletion.PROTECT, to='chul.CommunityHealthUnit'),
        ),
        migrations.AlterUniqueTogether(
            name='chuservicelink',
            unique_together=set([('chu', 'service')]),
        ),
    ]
