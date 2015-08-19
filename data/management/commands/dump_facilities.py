from django.core.management import BaseCommand

from facilities.models import Facility
import json

chunk_start = 0
chunk_size = 100


class Command(BaseCommand):
    def dump_facilities(self, chunk_start, chunk_size):
        records = []

        for fac in Facility.objects.all()[chunk_start:chunk_size]:
            data = {
                "code": fac.code,
                "name": fac.name,
                "official_name": fac.official_name,
                "created": fac.created.isoformat(),
                "location_desc": fac.location_desc,
                "plot_number": fac.plot_number,
                "number_of_beds": fac.number_of_beds,
                "number_of_cots": fac.number_of_cots,
                "facility_type": {"name": fac.facility_type.name},
                "owner": {"name": fac.owner.name}
            }
            if fac.town:
                data["town"] = {"name": fac.town.name}
            if fac.keph_level:
                data["keph_level"] = {"name": fac.keph_level.name}
            if fac.regulatory_body:
                data["regulatory_body"] = {"name": fac.regulatory_body.name}
            if fac.operation_status:
                data["operation_status"] = {"name": fac.operation_status.name}

            records.append(data)
        data_file = open(
            '/home/titan/savannah/mfl_api/data/new_data/facilities/{}_facilities.json'.format(chunk_start),
            'w+')
        fac_data = [
            {
                "model": "facilities.Facility",
                "unique_fields": [
                    "code"
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
