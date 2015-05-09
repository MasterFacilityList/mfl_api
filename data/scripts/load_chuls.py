import os
import csv
import json
from django.conf import settings
from facilities.models import Facility


chul_file = os.path.join(
    settings.BASE_DIR, 'data/csvs/chul.csv')

table_columns = [
    "CommUnitId", "Cu_code", "CommUnitName", "Date_CU_Established",
    "Date_CU_Operational", "CuLocation", "Link_Facility_Code",
    "CU_OfficialMobile", "CU_OfficialEmail", "Chew_Facility", "Chew_In_Charge",
    "NumHouseholds", "CUStatus", "Approved", "ApprovedDate", "ApprovedBy",
    "ApprovalComments", "isEdit", "UnitRecordArchived", "Date_added",
    "Date_modified", "Delete_comments"]


def create_chuls_file():  # noqa
    chul = []
    chews = []
    chu_contacts = []
    non_existing_facilities = []
    chul_codes = []
    chu_link_contacts = []

    with open(chul_file, 'r') as csv_file:
        chul_reader = csv.reader(csv_file)

        for row in chul_reader:
            try:
                Facility.objects.get(code=row[6])
            except:
                non_existing_facilities.append(row[6])
                continue

            code = row[1]
            name = row[2]
            date_established = row[3]
            facility_code = row[6]
            households_monitored = row[11]
            status = row[12]
            #  approval = row[13]

            #  contacts
            mobile = row[7]
            if mobile is not None and mobile != "NULL" and mobile != "":
                mobile_dict = {
                    "contact": mobile,
                    "contact_type": {
                        "name": "MOBILE"
                    }
                }
                chu_contact_link = {
                    "contact": mobile_dict,
                    "health_unit": {
                        "code": code
                    }
                }

                if chu_contact_link not in chu_link_contacts:
                    chu_link_contacts.append(chu_contact_link)
                if mobile_dict not in chu_contacts:
                    chu_contacts.append(mobile_dict)
            email = row[8]
            if email is not None and email != "NULL" and email != "":
                email_dict = {
                    "contact": email,
                    "contact_type": {
                        "name": "EMAIL"
                    }
                }
                chu_contact_email_link = {
                    "contact": email_dict,
                    "health_unit": {
                        "code": code
                    }
                }
                if chu_contact_email_link not in chu_link_contacts:
                    chu_link_contacts.append(chu_contact_email_link)

                if email_dict not in chu_contacts:
                    chu_contacts.append(email_dict)

            # chew
            first_name = row[10]
            if status == '1':
                status = {
                    "name": "Fully-functional"
                }
            if status == '2':
                status = {
                    "name": "semi-functional"
                }

            if status == '3':
                status = {
                    "name": "non-operational"
                }
            if date_established == "":
                date_established = "2000-01-01"
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

            if chu not in chul and code not in chul_codes:
                chul.append(chu)

            chul_codes.append(code)
            names = first_name.split()
            if len(names) > 1:
                first_name = names[0]
                last_name = names[1]
            else:
                first_name = name[0]
                last_name = ""

            chew = {
                "first_name": first_name,
                "last_name": last_name,
                "health_unit": {
                    "code": code
                }
            }
            if chew not in chews:
                chews.append(chew)

    return chul, chews, chu_contacts, chu_link_contacts


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
    chus, chews, chu_contacts, chu_link_contacts = create_chuls_file()
    write_file('chul.txt', chus)
    write_file('chew.txt', chews)
    write_file('chu_contacts.txt', chu_contacts)
    write_file('chu_link_contacts.txt', chu_link_contacts)
