import os
import csv
import json
from django.conf import settings
from facilities.models import Facility


facilities_file = os.path.join(
    settings.BASE_DIR, 'data/csvs/mfl_facilities.csv')


def read_the_facilities_file():  # noqa
    formatted_facilities = []
    email_contacts = []
    facilities_email_contacts = []
    fax_contacts = []
    facilities_fax_contacts = []
    mobile_contacts = []
    facilities_mobile_contacts = []
    postal_contacts = []
    facilities_postal_contacts = []
    land_line_contacts = []
    facilities_landline_contacts = []
    towns = []
    physical_addresss = []
    officers = []
    officers_contacts = []
    regulation_bodies = []
    facilities_regulation_statuses = []
    regulation_statuses = []
    job_titles = []
    facility_names = []

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
                try:
                    facility = Facility.objects.get(name=name)
                except:
                    facility = None

                # the child models
                # physical addrsss
                neartest_town = row[15]
                #  Town.objects.get_or_create(name=neartest_town)
                plot_number = row[16]
                address_town = row[29]
                postal_code = row[30]
                post_address = row[28]

                postal_contact = {
                    "contact_type": {
                        "name": "POSTAL"
                    },
                    "contact": "{} {} {}".format(
                        post_address, postal_code, address_town
                    )
                }
                if postal_contact not in postal_contacts:
                    postal_contacts.append(postal_contact)
                facility_postal_contact = {
                    "facility": {
                        "name": name
                    },
                    "contact": postal_contact

                }
                if facility_postal_contact not in facilities_postal_contacts and facility:  # NOQA
                    facilities_postal_contacts.append(facility_postal_contact)

                facility_physical_address = {
                    "town": {
                        "name": neartest_town
                    },
                    "plot_number": plot_number

                }
                town_dict = {"name": neartest_town}
                if town_dict not in towns:
                    towns.append(
                        {"name": neartest_town})
                if facility_physical_address not in physical_addresss and facility:  # NOQA
                    physical_addresss.append(facility_physical_address)
                facility_email = row[27]

                if facility_email:
                    email_contact = {
                        "contact_type": {
                            "name": "EMAIL"
                        },
                        "contact": facility_email
                    }
                    if email_contact not in email_contacts:
                        email_contacts.append(
                            email_contact
                        )
                    facility_email_contact = {
                        "facility": {
                            "name": name
                        },
                        "contact": email_contact
                    }
                    if facility_email_contact not in facilities_email_contacts and facility:  # NOQA
                        facilities_email_contacts.append(
                            facility_email_contact)
                facility_fax = row[25]
                if facility_fax:
                    fax_contact = {
                        "contact_type": {
                            "name": "FAX"
                        },
                        "contact": facility_fax
                    }
                    if fax_contact not in fax_contacts:
                        fax_contacts.append(fax_contact)
                    facility_fax_contact = {
                        "facility": {
                            "name": name
                        },
                        "contact": {
                            "contact": fax_contact
                        }

                    }
                    if facility_fax_contact not in facilities_fax_contacts and facility:  # NOQA
                        facilities_fax_contacts.append(facility_fax_contact)
                facility_mobile = row[26]
                if facility_mobile:
                    mobile_contact = {
                        "contact_type": {
                            "name": "MOBILE"
                        },
                        "contact": facility_mobile
                    }
                    if mobile_contact not in mobile_contacts:
                        mobile_contacts.append(mobile_contact)
                    facility_mobile_contact = {
                        "facility": {
                            "name": name
                        },
                        "contact": {
                            "contact": mobile_contact
                        }
                    }
                    if facility_mobile_contact not in facilities_mobile_contacts and facility:  # noqa
                        facilities_mobile_contacts.append(facility_mobile_contact)  # noqa
                facility_landline = row[24]
                if facility_landline:
                    landline_contact = {
                        "contact_type": {
                            "name": "LANDLINE"
                        },
                        "contact": facility_landline
                    }
                    if landline_contact not in land_line_contacts:
                        land_line_contacts.append(landline_contact)
                    facility_landline_contact = {
                        "facility": {
                            "name": name
                        },
                        "contact": landline_contact
                    }
                    if facility_landline_contact not in facilities_landline_contacts and facility:  # noqa
                        facilities_landline_contacts.append(
                            facility_landline_contact)

                officer_name = row[31]
                id_number = row[32]
                jobtitle = row[63]
                if (
                        officer_name and officer_name != ""
                        and jobtitle and jobtitle != ""):
                    officer_incharge = {
                        "name": officer_name,
                        "job_title": {
                            "name": jobtitle
                        },
                        "id_number": id_number

                    }
                    if {"name": jobtitle} not in job_titles:
                        job_titles.append({"name": jobtitle})
                    if officer_incharge not in officers:
                        officers.append(officer_incharge)

                # contacts
                officer_email = row[35]
                if officer_email:
                    officer_email_contact = {
                        "contact_type": {
                            "name": "EMAIL"
                        },
                        "contact": officer_email
                    }
                    if officer_email_contact not in email_contacts:
                        email_contacts.append(officer_email_contact)
                    officers_contact = {
                        "officer": officer_incharge,
                        "contact": officer_email_contact
                    }
                    if officers_contact not in officers_contacts:
                        officers_contacts.append(
                            officers_contact
                        )
                officer_personal_no = row[36]
                if officer_personal_no:
                    officer_personal_contact = {
                        "contact_type": {
                            "name": "MOBILE"
                        },
                        "contact": officer_personal_no
                    }
                    if officer_personal_contact not in mobile_contacts:
                        mobile_contacts.append(officer_personal_contact)
                    officers_thru_contact = {
                        "officer": officer_incharge,
                        "contact": {"contact": officer_personal_no}
                    }
                    if officers_thru_contact not in officers_contacts:
                        officers_contacts.append(
                            officers_thru_contact
                        )
                officer_mobile = row[34]
                if officer_mobile:
                    officer_mobile_contact = {
                        "contact_type": {
                            "name": "MOBILE"
                        },
                        "contact": officer_mobile
                    }
                    if officer_mobile_contact not in mobile_contacts:
                        mobile_contacts.append(officer_mobile_contact)

                    officer_incharge_thru_mobile = {
                        "officer": officer_incharge,
                        "contact": {"contact": officer_mobile}
                    }
                    if officer_incharge_thru_mobile not in officers_contacts:
                        officers_contacts.append(officer_incharge_thru_mobile)
                # regulators
                regulator_name = row[84]
                regulator_function = row[86]
                regulator_verb = row[87]
                regulator_abbreviation = row[83]
                if regulator_name and regulator_name != "":
                    regulator = {
                        "name": regulator_name,
                        "abbreviation": regulator_abbreviation,
                        "regulation_function": regulator_function,
                        "regulation_verb": regulator_verb
                    }
                    if regulator not in regulation_bodies:
                        regulation_bodies.append(regulator)
                # regulation statues
                regulation_status = row[87]
                if regulation_status and regulation_status != "":
                    if {"name": regulation_status} not in regulation_statuses:
                        regulation_statuses.append(
                            {"name": regulation_status})

                    # facility Regulation status
                    facility_regulation_status = {
                        "facility": {
                            "name": name
                        },
                        "regulating_body": {
                            "name": regulator_name
                        },
                        "regulation_status": {
                            "name": regulation_status
                        }

                    }
                    if facility_regulation_status not in facilities_regulation_statuses:  # noqa
                        facilities_regulation_statuses.append(
                            facility_regulation_status)

                code = row[3]
                description = row[45]
                location_desc = row[78]
                number_of_beds = row[43]
                number_of_cots = row[44]
                abbreviation = ""

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
                if facility_type and facility_type != "":
                    facility_type = facility_type
                else:
                    facility_type = "Other Hospital"

                operation_status = row[10]
                if not operation_status:
                    operation_status = "OPERATIONAL"

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
                    "attributes": json.dumps(attributes),
                    "physical_address": facility_physical_address

                }

                if name not in facility_names:
                    facility_names.append(name)
                    formatted_facilities.append(facility_dict)

            else:
                error_facilities.append(row)

        return {
            "formatted_facilities": formatted_facilities,
            "email_contacts": email_contacts,
            "facilities_email_contacts": facilities_email_contacts,
            "fax_contacts": fax_contacts,
            "facilities_fax_contacts": facilities_fax_contacts,
            "mobile_contacts": mobile_contacts,
            "facilities_mobile_contacts": facilities_mobile_contacts,
            "postal_contacts": postal_contacts,
            "facilities_postal_contacts": facilities_postal_contacts,
            "land_line_contacts": land_line_contacts,
            "facilities_landline_contacts": facilities_landline_contacts,
            "towns": towns,
            "physical_addresss": physical_addresss,
            "officers": officers,
            "officers_contacts": officers_contacts,
            "regulation_bodies": regulation_bodies,
            "facilities_regulation_statuses": facilities_regulation_statuses,
            "regulation_statuses": regulation_statuses,
            "error_facilities": error_facilities,
            "job_titles": job_titles
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
