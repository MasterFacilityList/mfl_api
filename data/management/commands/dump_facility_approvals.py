from django.core.management import BaseCommand

from facilities.models import Facility
import json

chunk_start = 0
chunk_size = 100


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        file_path = '/home/titan/savannah/mfl_api/data/new_data/demo_part_2/00_facility_approvals.json'
        data_file = open(file_path)
        data = data_file.read()
        records = json.loads(data)[0].get("records")
        new_records = []
        all_records = []

        index = 1
        for record in records:
            try:
                facility = Facility.objects.get(code=record.get("facility").get("code"))
                new_records.append(
                    {
                        "facility": {
                            "code": facility.code
                        }
                    }
                )
                print index
                index += 1
                all_records.append(new_records)
                if index == 100:
                    data = [{
                        "unique_fields": ["facility"],
                        "model": "facilities.FacilityApproval",
                        "records": new_records,
                    }]
                    new_records = []
                    new_file = open("/home/titan/savannah/mfl_api/data/new_data/approvals/{}_facility_approvals.json".format(len(all_records)), 'w+')
                    new_file.write(json.dumps(data))
                    new_file.close()
                    index = 1
            except:
                pass
