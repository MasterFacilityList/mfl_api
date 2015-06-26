import os
import csv
import json
from django.conf import settings
from facilities.models import Facility, Officer


facility_officers_file_file = os.path.join(
    settings.BASE_DIR, 'data/csvs/facility_officers_view.csv')


def read_the_facilities_file():
    formatted_facility_officers = []

    with open(facility_officers_file_file, 'r') as csv_file:
        facilities_reader = csv.reader(csv_file)
        col_names = [
            "Facility_Code", "In_Charge_Name",
            "In_Charge_National_ID", "In_Charge_Job_Title_ID",
            "ttlId", "ttlName"
        ]
        for row in facilities_reader:
            facility_code = row[0]
            officer_name = row[1]
            job_title = row[5]
            facility_officer_dict = {
                "facility": {
                    "code": facility_code
                },
                "officer": {
                    "name": officer_name
                }

            }
            try:
                try:
                    Officer.objects.get(name=officer_name)
                    Facility.objects.get(code=str(facility_code))
                    if facility_officer_dict not in formatted_facility_officers:
                        formatted_facility_officers.append(facility_officer_dict)
                    # print facility_officer_dict
                except (Officer.MultipleObjectsReturned):
                    # print "Officer with name {} does not exist".format(officer_name)
                    pass

            except:
                # print "Facility with code {} does not exist".format(facility_code)
                pass
    return {
        "officers": formatted_facility_officers
    }


def write_file(file_name, data):
    if os.path.exists(file_name):
        os.remove(file_name)
    fac_file = open(file_name, 'w+')
    del data[0]
    dumped_data = ""
    try:
        dumped_data = json.dumps(data)
    except:
        print data
        raise

    fac_file.write(dumped_data)


def write_jsons_to_file():
    data = read_the_facilities_file()
    keys = data.keys()

    for key in keys:
        entity_data = data.get(key)
        file_name = key + "{}".format('.txt')
        write_file(file_name, entity_data)
