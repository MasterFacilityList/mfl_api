# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_auto_20150413_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategory',
            name='name',
            field=models.CharField(default='no name', help_text=b'What is the name of the category? ', max_length=100),
            preserve_default=False,
        ),
    ]
