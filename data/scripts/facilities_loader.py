import os
import csv
import json
from django.conf import settings
from facilities.models import FacilityType, FacilityStatus, Officer, OfficerContact

from common.models import ContactType, Town, PhyicalAddress

facilities_file = os.path.join(
    settings.BASE_DIR, 'data/csvs/mfl_facilities.csv')


def read_the_facilities_file():  # noqa
    formatted_facilities = []
    email_contacts = []
    facilities_email_contacts = []
    fax_contacts = []
    facilities_fax_contacts = []
    mobile_contact = []
    facilities_mobile_contacts = []
    postal_contacts = []
    facilities_postal_contacts = []
    land_line_contacts = []
    facilities_landline_contacts = []

    with open(facilities_file, 'r') as csv_file:
        facilities_reader = csv.reader(csv_file)
        col_names = [  # noqa
            'ID_FACILITY', 'Facility_TransactionID', 'Facility_DataEntryStatus',  # noqa
            'Facility_Code', 'Facility_Name', 'Facility_District_ID', 'Facility_Type_ID',  # noqa
            'Facility_Owner_ID', 'Facility_Op_Status_ID', 'Facility_Reg_Status_ID',  # noqa
            'Facility_Gazette_By_ID', 'Facility_Constituency_ID', 'Facility_Division',  # noqa
            'Facility_Location', 'Facility_SubLocation', 'Facility_Nearest_Town',  # noqa
            'Facility_Plot_Number', 'Facility_Latitude', 'Facility_Longitude',
            'Source_of_GeoCode', 'Method_of_GeoCode', 'Date_of_GeoCode',  # noqa
            'Facility_Date_Start', 'Facility_Date_End', 'Official_Landline',
            'Official_Fax', 'Official_Mobile', 'Official_Email',  # noqa
            'Official_Address', 'Official_Address_Town',  # noqa
            'Official_Address_PostCode', 'In_Charge_Name',
            'In_Charge_National_ID', 'In_Charge_Job_Title_ID',  # noqa
            'In_Charge_Mobile', 'In_Charge_Email',  # noqa
            'In_Charge_Pers_Num', 'In_Charge_National_ID_1',  # noqa
            'In_Charge_Name_1', 'In_Charge_Job_Title_ID_1', 'In_Charge_Mobile_1',  # noqa
            'In_Charge_Email_1', 'In_Charge_Pers_Num_1', 'Num_Beds', 'Num_Cots',  # noqa
            'Notes', 'Reg_Date', 'Reg_Ref_Number', 'Date_Added', 'disId',  # noqa
            'disName', 'prvId', 'prvName', 'conId', 'conName', 'typId',  # noqa
            'typName', 'typParent', 'geoId', 'geoName', 'ownId', 'ownName',  # noqa
            'ownParent', 'ttlName', 'ttlId', 'ttlID_1', 'ttlName_1',
            'RecordArchived', 'Open24Hours', 'OpenWeekends', 'Facility_Keph_ID',  # noqa
            'Facility_RegisteredBy_Organization_ID', 'Facility_Official_Name',
            'RegisteredByName', 'kphName', 'AddedByUsrId', 'Facility_Regulator_ID',  # noqa
            'Facility_Regulatory_Status_ID', 'Location_Description', 'Official_Alternate_Number',  # noqa
            'Official_Post', 'PP_Registration_No', 'regId', 'regShortName', 'regName',  # noqa
            'regDisplayName', 'regDefaultStatus', 'regFunction', 'regFunctionVerb',  # noqa
            'regAddress', 'Approved', 'ApprovedByUsrId', 'ApprovedDate', 'staId',  # noqa
            'staDisplayName', 'Date_Modified', 'IsEdit', 'RgnId', 'RgnName']  # noqa
        error_facilities = []
        for row in facilities_reader:
            if len(row) == 99:
                name = row[4]
                # the child models
                # physical addrsss
                neartest_town = row[15]
                Town.objects.get_or_create(name=neartest_town)
                plot_number = row[16]
                address_town = row[29]
                postal_code = row[30]
                post_address = row[28]
                facility_postal_contact = {

                }

                physical_addresss = PhyicalAddress.objects.get_or_create(
                    town=neartest_town, plot_number=plot_number)

                facility_pysical_address = {
                    "town": neartest_town,
                    "plot_number": plot_number

                }
                facility_email = row[27]

                if facility_email:
                    email_contact = {
                        "contact_type": "EMAIL",
                        "contact": facility_email
                    }
                    email_contacts.append(
                        email_contact
                    )
                    facility_email_contact = {
                        "facility": name,
                        "contact": email_contact

                    }
                    facilities_email_contacts.append(
                        facility_email_contact)
                facility_fax = row[25]
                if facility_fax:
                    fax_contact = {
                        "contact_type": "FAX",
                        "contact": facility_fax
                    }
                    facility_fax_contact = {
                        "facility": name,
                        "contact": fax_contact

                    }
                    facilities_fax_contacts.append(facility_fax_contact)
                facility_mobile = row[26]
                if facility_mobile:
                    mobile_contact = {
                        "contact_type": "MOBILE",
                        "contact": facility_mobile
                    }
                    facility_mobile_contact = {
                        "facility": name,
                        "contact": mobile_contact

                    }
                    facilities_mobile_contacts.append(facility_mobile_contact)
                facility_landline = row[24]
                if facility_landline:
                    landline_contact = {
                        "contact_type": "LANDLINE",
                        "contact": facility_landline
                    }
                    facility_landline_contact = {

                    }
                code = row[3]
                description = row[45]
                location_desc = row[78]
                number_of_beds = row[43]
                number_of_cots = row[44]
                abbreviation = row[83]

                if number_of_cots == "" or not number_of_cots or number_of_cots == "Num_Cots":  # noqa
                    number_of_cots = 0
                else:
                    number_of_cots = int(number_of_cots)

                if number_of_beds == "" or not number_of_beds or number_of_beds == "Num_Beds":  # noqa
                    number_of_beds = 0
                else:
                    number_of_beds = int(number_of_beds)

                open_whole_day = row[68]
                open_whole_week = row[69]

                if open_whole_day == "0":
                    open_whole_day = False
                else:
                    open_whole_day = True

                if open_whole_week == "0":
                    open_whole_week = False
                else:
                    open_whole_week = True

                is_published = row[90]

                if is_published:
                    is_published = True
                facility_type = row[56]
                FacilityType.objects.get_or_create(name=facility_type)
                operation_status = row[10]
                if not operation_status:
                    operation_status = "OPERATIONAL"
                try:
                    FacilityStatus.objects.get_or_create(
                        name=operation_status, description="some desc")
                except:
                    pass

                owner = row[61]
                attributes = {
                    "location": row[13],
                    "division": row[12],
                    "sub_location": row[14],
                    "latitude": row[17],
                    "longitude": row[18],
                }
                facility_dict = {
                    "name": name,
                    "code": code,
                    "abbreviation": abbreviation,
                    "description": description,
                    "location_desc": location_desc,
                    "number_of_beds": number_of_beds,
                    "number_of_cots": number_of_cots,
                    "open_whole_day": open_whole_day,
                    "open_whole_week": open_whole_week,
                    "is_published": is_published,
                    "facility_type": {
                        "name": facility_type
                    },
                    "operation_status": {
                        "name": operation_status
                    },
                    "owner": {
                        "name": owner
                    },
                    "attributes": json.dumps(attributes)

                }
                formatted_facilities.append(facility_dict)
            else:
                error_facilities.append(row)

        return formatted_facilities, error_facilities


def write_to_file():
    if os.path.exists('facilities.txt'):
        os.remove('facilities.txt')
    fac_file = open('facilities.txt', 'w+')
    data = read_the_facilities_file()
    data = data[0]
    del data[0]
    fac_file.write(json.dumps(data))
