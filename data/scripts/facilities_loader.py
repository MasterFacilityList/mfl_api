import os
import csv
from django.conf import settings

from facilities.models import FacilityType, Owner, FacilityStatus, Officer, OfficerContact

facilities_file = os.path.join(
    settings.BASE_DIR, 'data/csvs/mfl_facilities.csv')


def read_the_facilities_file():
    with open(facilities_file, 'r') as csv_file:
        facilities_reader = csv.reader(csv_file)
        for row in facilities_reader:
            import pdb
            pdb.set_trace()
            name = row[4]
            code = row[3]
            description = row[48]
            location_desc = row[17]
            number_of_beds = row[46]
            number_of_cots = row[47]

            if number_of_cots == "":
                number_of_cots = 0

            open_whole_day = row[49]
            open_whole_week = row[50]
            is_published = row[59]

            if is_published:
                is_published = True
            facility_type = row[7]
            operation_status = row[10]
            owner = row[9]
            facility_dict = {
                "name": name,
                "code": code,
                "descritption": description,
                "location_desc": location_desc,
                "number_of_beds": number_of_beds,
                "number_of_cots": number_of_cots,
                "open_whole_day": open_whole_day,
                "open_whole_Week": open_whole_week,
                "is_published": is_published,
                "facility_type": facility_type,
                "operation_status": operation_status,
                "owner": owner

            }
            print facility_dict
            facility_type_object = FacilityType.objects.get(name=facility_type)
            owner_object = Owner.objects.get(name=owner)
            officer_in_charge_object = Officer.objects.get(id_number=id_number)
            officer_contact_object = ""

            # officer incharge
            # practitioners
            # physical address
            # officer in charge contacts
            # officer_in_charge
            # physical_address
