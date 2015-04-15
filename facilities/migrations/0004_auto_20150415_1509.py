# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import common.models.base
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0003_remove_facilityservice_service_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityCoordinates',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('latitude', models.CharField(help_text=b'How far north or south a facility is from the equator', max_length=255)),
                ('longitude', models.CharField(help_text=b'How far east or west one a facility is from the Greenwich Meridian', max_length=255)),
                ('collection_date', models.DateTimeField()),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'facility coordinates',
                'verbose_name_plural': 'facility coordinates',
            },
        ),
        migrations.RemoveField(
            model_name='facilitygps',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='facilitygps',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='facilitygps',
            name='method',
        ),
        migrations.RemoveField(
            model_name='facilitygps',
            name='source',
        ),
        migrations.RemoveField(
            model_name='facilitygps',
            name='updated_by',
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'verbose_name_plural': 'facilities'},
        ),
        migrations.AlterModelOptions(
            name='facilityregulationstatus',
            options={'verbose_name_plural': 'facility regulation statuses'},
        ),
        migrations.AlterModelOptions(
            name='facilityservice',
            options={'verbose_name_plural': 'facility services'},
        ),
        migrations.AlterModelOptions(
            name='facilitystatus',
            options={'verbose_name_plural': 'facility statuses'},
        ),
        migrations.AlterModelOptions(
            name='officerincharge',
            options={'verbose_name_plural': 'officers in charge'},
        ),
        migrations.AlterModelOptions(
            name='regulatingbody',
            options={'verbose_name_plural': 'regulating bodies'},
        ),
        migrations.AlterModelOptions(
            name='regulationstatus',
            options={'verbose_name_plural': 'regulation_statuses'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name_plural': 'services'},
        ),
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'verbose_name_plural': 'service categories'},
        ),
        migrations.DeleteModel(
            name='FacilityGPS',
        ),
        migrations.AddField(
            model_name='facilitycoordinates',
            name='facility',
            field=models.OneToOneField(to='facilities.Facility'),
        ),
        migrations.AddField(
            model_name='facilitycoordinates',
            name='method',
            field=models.ForeignKey(help_text=b'Method used to obtain the geo codes. e.g taken with GPS device', to='facilities.GeoCodeMethod'),
        ),
        migrations.AddField(
            model_name='facilitycoordinates',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.GeoCodeSource', help_text=b'where the geo code came from'),
        ),
        migrations.AddField(
            model_name='facilitycoordinates',
            name='updated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.PROTECT, default=common.models.base.get_default_system_user_id, to=settings.AUTH_USER_MODEL),
        ),
    ]
