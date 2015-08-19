from django.core.management import BaseCommand

from mfl_gis.models import FacilityCoordinates
import json

chunk_start = 0
chunk_size = 100


class Command(BaseCommand):
    def dump_facilities(self, chunk_start, chunk_size):
        records = []
        for fac in FacilityCoordinates.objects.all()[chunk_start:chunk_size]:

            data = {
                "facility": {
                    "code": fac.facility.code
                },
                "source": {
                    "name": fac.source.name
                },
                "method": {
                    "name": fac.method.name
                },
                "collection_date": fac.created.isoformat(),
                "coordinates": json.dumps({
                    "type": "Point",
                    "coordinates": [
                        fac.coordinates[0],
                        fac.coordinates[1]]
                }),
            }

            records.append(data)
        data_file = open(
            '/home/titan/savannah/mfl_api/data/new_data/geocodes/{}_facility_cords.json'.format(chunk_start),  # NOQA
            'w+')
        fac_data = [
            {
                "model": "mfl_gis.FacilityCoordinates",
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
        iterations = FacilityCoordinates.objects.count() / chunk_size
        while iteration_count < iterations:
            chunk_start = chunk_size * iteration_count
            self.dump_facilities(chunk_start + 1, chunk_size + chunk_start)
            iteration_count += 1
