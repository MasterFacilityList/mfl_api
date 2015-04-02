# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InchargeCounties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('county', models.ForeignKey(to='common.County')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('contact', models.ForeignKey(to='common.Contact')),
                ('county', models.ForeignKey(to='common.County')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='mfluser',
            name='is_incharge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='created_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='updated_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userdetail',
            name='user',
            field=models.ForeignKey(related_name='user_detail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inchargecounties',
            name='created_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inchargecounties',
            name='updated_by',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inchargecounties',
            name='user',
            field=models.ForeignKey(related_name='counties', to=settings.AUTH_USER_MODEL),
        ),
    ]
