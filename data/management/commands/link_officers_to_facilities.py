import json
import os
import logging

from facilities.models import Facility, Officer, FacilityOfficer
from users.models import MflUser
from django.core.management import BaseCommand
from django.core.exceptions import ValidationError
from django.conf import settings

system_user = MflUser.objects.get(email='system@ehealth.or.ke')


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        file_path = os.path.join(
            settings.BASE_DIR,
            'data/data/msc/facility_officer_in_charge_link.json')
        with open(file_path) as ops_data:
            data = json.load(ops_data)
            records = data[0].get('records')
            for record in records:
                try:
                    facility = Facility.objects.get(code=record.get('code'))
                    officer = Officer.objects.filter(
                        name=str(
                            record.get('name').encode('utf-8').strip()))[0]
                    try:
                        print FacilityOfficer.objects.create(
                            facility=facility, officer=officer,
                            created_by=system_user, updated_by=system_user)
                    except ValidationError:
                        print facility, officer
                except Facility.DoesNotExist:
                    logger.info("The facility {} does not exist".format(
                        record.get('code')))
                    continue
                except IndexError:
                    logger.info("The Officer {} does not exist".format(
                        record.get('name')))
                    continue
                except AttributeError:
                    logger.info(record)
