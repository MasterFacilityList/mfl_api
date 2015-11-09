import json
import os
import logging

from facilities.models import Facility

from django.core.management import BaseCommand
from django.conf import settings


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        file_path = os.path.join(
            settings.BASE_DIR,
            'data/data/msc/facility_hours_of_operation.json')
        with open(file_path) as ops_data:
            data = json.load(ops_data)
            records = data[0].get('records')
            for record in records:
                try:
                    facility = Facility.objects.get(code=record.get('code'))
                    open_24_hours = record.get('open_24_hours', None)
                    open_weekends = record.get('open_weekends', None)
                    if open_24_hours == 1:
                        facility.open_whole_day = True
                    if open_weekends == 1:
                        facility.open_weekends = True
                    facility.save(allow_save=True)
                except Facility.DoesNotExist:
                    logger.info("The facility {} does not exist".format(
                        record.get('code')))
                    continue
