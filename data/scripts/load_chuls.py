import os
import csv
import json
from django.conf import settings


chul_file = os.path.join(
    settings.BASE_DIR, 'data/csvs/chul.csv')

table_columns = [
    "CommUnitId", "Cu_code", "CommUnitName", "Date_CU_Established",
    "Date_CU_Operational", "CuLocation", "Link_Facility_Code",
    "CU_OfficialMobile", "CU_OfficialEmail", "Chew_Facility", "Chew_In_Charge",
    "NumHouseholds", "CUStatus", "Approved", "ApprovedDate", "ApprovedBy",
    "ApprovalComments", "isEdit", "UnitRecordArchived", "Date_added",
    "Date_modified", "Delete_comments"]


def create_chuls_file():
    chul = []
    chews = []
    chu_contacts = []
    with open(chul_file, 'r') as csv_file:
        chul_reader = csv.reader(csv_file)

        for row in chul_reader:
            code = row[1]
            name = row[2]
            date_established = row[3]
            facility_code = row[7]
            households_monitored = row[11]
            status = row[12]
            #  approval = row[13]

            #  contacts
            mobile = row[7]
            mobile_dict = {
                "contact": mobile,
                "contact_type": {
                    "PHONE"
                }
            }
            email = row[8]
            email_dict = {
                "contact": email,
                "contact_type": {
                    "EMAIL"
                }
            }
            if email_dict not in chu_contacts:
                chu_contacts.append(email_dict)
            if mobile_dict not in chu_contacts:
                chu_contacts.append(email_dict)

            # chew
            first_name = row[10]

            chu = {
                "code": code,
                "name": name,
                "date_established": date_established,
                "facility": {
                    "code": facility_code
                },
                "households_monitored": households_monitored,
                "status": status,
            }
            if chu not in chul:
                chul.append(chu)

            chew = {
                "first_name": first_name,
                "heath_unit": {
                    "code": code
                }
            }
            if chew not in chews:
                chews.append(chew)

    return chul, chews


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


def write_chuls_and_chews():
    chus, chews = create_chuls_file()
    write_file('chul.txt', chus)
    write_file('chew.txt', chews)
