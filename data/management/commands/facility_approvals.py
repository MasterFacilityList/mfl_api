import json

from django.core.management import BaseCommand

from mfl_gis.models import Facility

chunk_start = 0
chunk_size = 100


class Command(BaseCommand):
    def dump_facilities(self, chunk_start, chunk_size):
        records = []
        for fac in Facility.objects.all()[chunk_start:chunk_size]:

            data = {
                "facility": {
                    "code": fac.code
                }
            }

            records.append(data)
        data_file = open(
            '/home/titan/savannah/mfl_api/data/new_data/approvals/{}_facility_approvals.json'.format(chunk_start),  # NOQA
            'w+')
        fac_data = [
            {
                "model": "facilities.FacilityApproval",
                "unique_fields": [
                    "facility"
                ],
                "records":records
            }
        ]
        data_file.write(json.dumps(fac_data))
        data_file.close()

    def handle(self, *args, **kwargs):
        iteration_count = 0
        iterations = Facility.objects.count() / chunk_size
        while iteration_count < iterations:
            chunk_start = chunk_size * iteration_count
            self.dump_facilities(chunk_start + 1, chunk_size + chunk_start)
            iteration_count += 1
