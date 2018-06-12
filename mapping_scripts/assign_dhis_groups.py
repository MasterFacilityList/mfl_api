#!/home/elon/.virtualenv/mfl_api python2.7

from conn import myConnection as conn
import requests
import base64
from datetime import datetime


url = "https://test.hiskenya.org/dev/api/"
cred = base64.b64encode("healthit:hEALTHIT2017")


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def log(data):
    with open("logs.txt", 'a+') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+": "+str(data)+"\n")
        f.close()


def get_org_unit_group_payload(org_unit_group_id):
    r = requests.get(
        url+"organisationUnitGroups/"+org_unit_group_id,
        headers={
            "Authorization": "Basic " + cred,
            "Accept": "application/json"
        },
        params={
            "fields": "[*]",
            "paging": "false"
        }
    )

    return r.json()


def assign_org_unit_to_group(org_unit_id, org_unit_group_id):
    org_unit_group_payload = get_org_unit_group_payload(org_unit_group_id)
    org_unit_group_payload["organisationUnits"].append({"id": org_unit_id})

    r = requests.put(
        url + "organisationUnitGroups/" + org_unit_group_id,
        headers={
            "Authorization": "Basic " + cred,
            "Accept": "application/json"
        },
        json=org_unit_group_payload
    )

    if str(r.status_code) == "200":
        return "Group assignment completed successfully!"
    else:
        return "Group assignment unsuccessful"


def org_unit_uid(mfl_code):
    r = requests.get(
        url+"organisationUnits",
        headers={
            "Authorization": "Basic " + cred,
            "Accept": "application/json"
        },
        params={
            "filter": "code:eq:"+str(mfl_code),
            "fields": "[id]",
            "paging": "false"
        }
    )

    log (r.json())

    data = r.json()["organisationUnits"]

    if len(data) is 0:
        return None
    else:
        return data[0]["id"]


def process_org_unit_groups_for_each_facility():

    # stats stuff
    sts_percentage_complete = 0
    sts_facilities_processed_count = 0
    sts_facilities_with_group_facility_type_count = 0
    sts_facilities_with_group_keph_level_count = 0
    sts_facilities_with_group_facility_owner_count = 0
    sts_facilities_with_group_regulatory_body_count = 0
    sts_facilities_with_group_facility_owner_type_count = 0
    sts_facilities_with_group_facility_type_skipped_count = 0
    sts_facilities_with_group_keph_level_skipped_count = 0
    sts_facilities_with_group_facility_owner_skipped_count = 0
    sts_facilities_with_group_regulatory_body_skipped_count = 0
    sts_facilities_with_group_facility_owner_type_skipped_count = 0

    cur_select = conn.cursor()
    cur_select.execute("SELECT COUNT(*) FROM facilities_facility")

    sts_all_facilities_count = cur_select.fetchone()[0]

    query = "SELECT f.code AS mfl_code,"\
            "  f.name AS facility_name,"\
            "  ft.name AS facility_type,"\
            "  cogm_ft.dhis_id As facility_type_dhis_id,"\
            "  fk.name AS keph_level,"\
            "  cogm_fk.dhis_id As keph_level_dhis_id,"\
            "  fo.name AS facility_owner,"\
            "  cogm_fo.dhis_id As facility_owner_dhis_id,"\
            "  frb.name AS regulatory_body,"\
            "  cogm_frb.dhis_id As regulatory_body_dhis_id,"\
            "  fot.name AS facility_owner_type,"\
            "  cogm_fot.dhis_id As facility_owner_type_dhis_id"\
            " FROM facilities_facility AS f"\
            " LEFT JOIN facilities_facilitytype AS ft ON f.facility_type_id = ft.id"\
            " LEFT JOIN common_orgunitgroupsmapping AS cogm_ft ON cogm_ft.mfl_name = ft.name"\
            " LEFT JOIN facilities_kephlevel AS fk ON f.keph_level_id = fk.id"\
            " LEFT JOIN common_orgunitgroupsmapping AS cogm_fk ON cogm_fk.mfl_name = 'KEPH ' || fk.name"\
            " LEFT JOIN facilities_owner AS fo ON f.owner_id = fo.id"\
            " LEFT JOIN common_orgunitgroupsmapping AS cogm_fo ON cogm_fo.mfl_name = fo.name"\
            " LEFT JOIN facilities_regulatingbody AS frb ON f.regulatory_body_id = frb.id"\
            " LEFT JOIN common_orgunitgroupsmapping AS cogm_frb ON cogm_frb.mfl_name = frb.name"\
            " LEFT JOIN facilities_ownertype AS fot ON fo.owner_type_id = fot.id"\
            " LEFT JOIN common_orgunitgroupsmapping AS cogm_fot ON cogm_fot.mfl_name = fot.name"\
            " WHERE cogm_ft.dhis_id IS NOT NULL"\
            " AND cogm_fk.dhis_id IS NOT NULL"\
            " AND cogm_fo.dhis_id IS NOT NULL"\
            " AND cogm_frb.dhis_id IS NOT NULL"\
            " AND cogm_fot.dhis_id IS NOT NULL"\
            " ORDER BY f.code ASC"

    cur_select.execute(query)

    for mfl_code,    \
        facility_name,\
        facility_type, \
        facility_type_dhis_id,\
        keph_level, \
        keph_level_dhis_id,\
        facility_owner, \
        facility_owner_dhis_id,\
        regulatory_body, \
        regulatory_body_dhis_id,\
        facility_owner_type, \
        facility_owner_type_dhis_id\
            in cur_select.fetchall():

        log ("\nProcessing Facility - "+facility_name+" ("+str(mfl_code)+")\n"
               "--------\n")
        dhis2_uid = org_unit_uid(mfl_code)
        if dhis2_uid is None:
            log("Skipping Facility...")
            continue
        else:
            log("DHIS2 Facility UID: "+str(dhis2_uid)+"\n")
            sts_facilities_processed_count +=1

        sts_facilities_with_group_facility_type_count +=1
        if facility_type is None:
            sts_facilities_with_group_facility_type_skipped_count +=1
            log("Skipping Facility Type... \n")
        else:
            log("Facility Type - " + facility_type)
            log("DHIS2 ID: "+str(facility_type_dhis_id)+"\nAssigning Organisation Unit Group...")
            log(assign_org_unit_to_group(dhis2_uid, facility_type_dhis_id)+"\n")

        sts_facilities_with_group_keph_level_count +=1
        if keph_level is None:
            sts_facilities_with_group_keph_level_skipped_count +=1
            log("Skipping KEPH Level... \n")
        else:
            log("KEPH Level - " + keph_level)
            log("DHIS2 ID: "+str(keph_level_dhis_id)+"\nAssigning Organisation Unit Group...")
            log(assign_org_unit_to_group(dhis2_uid, keph_level_dhis_id) + "\n")

        sts_facilities_with_group_facility_owner_count +=1
        if facility_owner is None:
            sts_facilities_with_group_facility_owner_skipped_count +=1
            log("Skipping Facility Owner... \n")
        else:
            log("Facility Owner - " + facility_owner)
            log("DHIS2 ID: "+str(facility_owner_dhis_id)+"\nAssigning Organisation Unit Group...")
            log(assign_org_unit_to_group(dhis2_uid, facility_owner_dhis_id) + "\n")

        sts_facilities_with_group_regulatory_body_count +=1
        if regulatory_body is None:
            sts_facilities_with_group_regulatory_body_skipped_count +=1
            log("Skipping Regulatory Body... \n")
        else:
            log("Regulatory Body - " + regulatory_body)
            log("DHIS2 ID: "+str(regulatory_body_dhis_id)+"\nAssigning Organisation Unit Group...")
            log(assign_org_unit_to_group(dhis2_uid, regulatory_body_dhis_id) + "\n")

        sts_facilities_with_group_facility_owner_type_count +=1
        if facility_owner_type is None:
            sts_facilities_with_group_facility_owner_type_skipped_count +=1
            log("Skipping Facility Owner Type... \n")
        else:
            log("Facility Owner Type - " + facility_owner_type)
            log("DHIS2 ID: "+str(facility_owner_type_dhis_id)+"\nAssigning Organisation Unit Group...")
            log(assign_org_unit_to_group(dhis2_uid, facility_owner_type_dhis_id) + "\n")

        print("Interim Statistics:")
        print("----")

        print("Percentage Complete: "+str((float(sts_facilities_processed_count)/float(sts_all_facilities_count))*100)+"%")
        print("Total Facilities: "+str(sts_all_facilities_count))
        print("Facilities Proccessed: "+str(sts_facilities_processed_count))

        print("sts_facilities_with_group_facility_type_count :"+str(sts_facilities_with_group_facility_type_count))
        print("sts_facilities_with_group_keph_level_count :"+str(sts_facilities_with_group_keph_level_count))
        print("sts_facilities_with_group_facility_owner_count :"+str(sts_facilities_with_group_facility_owner_count))
        print("sts_facilities_with_group_regulatory_body_count :"+str(sts_facilities_with_group_regulatory_body_count))
        print("sts_facilities_with_group_facility_owner_type_count :"+str(sts_facilities_with_group_facility_owner_type_count))

        print("sts_facilities_with_group_facility_type_processed_count :"+str(sts_facilities_with_group_facility_type_count-sts_facilities_with_group_facility_type_skipped_count))
        print("sts_facilities_with_group_keph_level_processed_count :"+str(sts_facilities_with_group_keph_level_count-sts_facilities_with_group_keph_level_skipped_count))
        print("sts_facilities_with_group_facility_owner_processed_count :"+str(sts_facilities_with_group_facility_owner_count-sts_facilities_with_group_facility_owner_skipped_count))
        print("sts_facilities_with_group_regulatory_body_processed_count :"+str(sts_facilities_with_group_regulatory_body_count-sts_facilities_with_group_regulatory_body_skipped_count))
        print("sts_facilities_with_group_facility_owner_type_processed_count :"+str(sts_facilities_with_group_facility_owner_type_count-sts_facilities_with_group_facility_owner_type_skipped_count))

        print("sts_facilities_with_group_facility_type_skipped_count :"+str(sts_facilities_with_group_facility_type_skipped_count))
        print("sts_facilities_with_group_keph_level_skipped_count :"+str(sts_facilities_with_group_keph_level_skipped_count))
        print("sts_facilities_with_group_facility_owner_skipped_count :"+str(sts_facilities_with_group_facility_owner_skipped_count))
        print("sts_facilities_with_group_regulatory_body_skipped_count :"+str(sts_facilities_with_group_regulatory_body_skipped_count))
        print("sts_facilities_with_group_facility_owner_type_skipped_count :"+str(sts_facilities_with_group_facility_owner_type_skipped_count)+"\n\n")

        log("Interim Statistics:")
        log("----")

        log("Percentage Complete: " + str(
            (float(sts_facilities_processed_count) / float(sts_all_facilities_count)) * 100) + "%")
        log("Total Facilities: " + str(sts_all_facilities_count))
        log("Facilities Proccessed: " + str(sts_facilities_processed_count))

        log("sts_facilities_with_group_facility_type_count :" + str(sts_facilities_with_group_facility_type_count))
        log("sts_facilities_with_group_keph_level_count :" + str(sts_facilities_with_group_keph_level_count))
        log("sts_facilities_with_group_facility_owner_count :" + str(sts_facilities_with_group_facility_owner_count))
        log(
        "sts_facilities_with_group_regulatory_body_count :" + str(sts_facilities_with_group_regulatory_body_count))
        log("sts_facilities_with_group_facility_owner_type_count :" + str(
            sts_facilities_with_group_facility_owner_type_count))

        log("sts_facilities_with_group_facility_type_processed_count :" + str(
            sts_facilities_with_group_facility_type_count - sts_facilities_with_group_facility_type_skipped_count))
        log("sts_facilities_with_group_keph_level_processed_count :" + str(
            sts_facilities_with_group_keph_level_count - sts_facilities_with_group_keph_level_skipped_count))
        log("sts_facilities_with_group_facility_owner_processed_count :" + str(
            sts_facilities_with_group_facility_owner_count - sts_facilities_with_group_facility_owner_skipped_count))
        log("sts_facilities_with_group_regulatory_body_processed_count :" + str(
            sts_facilities_with_group_regulatory_body_count - sts_facilities_with_group_regulatory_body_skipped_count))
        log("sts_facilities_with_group_facility_owner_type_processed_count :" + str(
            sts_facilities_with_group_facility_owner_type_count - sts_facilities_with_group_facility_owner_type_skipped_count))

        log("sts_facilities_with_group_facility_type_skipped_count :" + str(
            sts_facilities_with_group_facility_type_skipped_count))
        log("sts_facilities_with_group_keph_level_skipped_count :" + str(
            sts_facilities_with_group_keph_level_skipped_count))
        log("sts_facilities_with_group_facility_owner_skipped_count :" + str(
            sts_facilities_with_group_facility_owner_skipped_count))
        log("sts_facilities_with_group_regulatory_body_skipped_count :" + str(
            sts_facilities_with_group_regulatory_body_skipped_count))
        log("sts_facilities_with_group_facility_owner_type_skipped_count :" + str(
            sts_facilities_with_group_facility_owner_type_skipped_count))

    print("Final Statistics:")
    print("----")

    print("Percentage Complete: " + str((float(sts_facilities_processed_count) / float(sts_all_facilities_count)) * 100)+"%")
    print("Total Facilities: " + str(sts_all_facilities_count))
    print("Facilities Proccessed: " + str(sts_facilities_processed_count))

    print("sts_facilities_with_group_facility_type_processed_count :" + str(sts_facilities_with_group_facility_type_count - sts_facilities_with_group_facility_type_skipped_count))
    print("sts_facilities_with_group_keph_level_processed_count :" + str(sts_facilities_with_group_keph_level_count - sts_facilities_with_group_keph_level_skipped_count))
    print("sts_facilities_with_group_facility_owner_processed_count :" + str(sts_facilities_with_group_facility_owner_count - sts_facilities_with_group_facility_owner_skipped_count))
    print("sts_facilities_with_group_regulatory_body_processed_count :" + str(sts_facilities_with_group_regulatory_body_count - sts_facilities_with_group_regulatory_body_skipped_count))
    print("sts_facilities_with_group_facility_owner_type_processed_count :" + str(sts_facilities_with_group_facility_owner_type_count - sts_facilities_with_group_facility_owner_type_skipped_count))

    print("sts_facilities_with_group_facility_type_count :" + str(sts_facilities_with_group_facility_type_count))
    print("sts_facilities_with_group_keph_level_count :" + str(sts_facilities_with_group_keph_level_count))
    print("sts_facilities_with_group_facility_owner_count :" + str(sts_facilities_with_group_facility_owner_count))
    print("sts_facilities_with_group_regulatory_body_count :" + str(sts_facilities_with_group_regulatory_body_count))
    print("sts_facilities_with_group_facility_owner_type_count :" + str(sts_facilities_with_group_facility_owner_type_count))

    print("sts_facilities_with_group_facility_type_skipped_count :" + str(sts_facilities_with_group_facility_type_skipped_count))
    print("sts_facilities_with_group_keph_level_skipped_count :" + str(sts_facilities_with_group_keph_level_skipped_count))
    print("sts_facilities_with_group_facility_owner_skipped_count :" + str(sts_facilities_with_group_facility_owner_skipped_count))
    print("sts_facilities_with_group_regulatory_body_skipped_count :" + str(sts_facilities_with_group_regulatory_body_skipped_count))
    print("sts_facilities_with_group_facility_owner_type_skipped_count :" + str(sts_facilities_with_group_facility_owner_type_skipped_count))

    log("Final Statistics:")
    log("----")

    log("Percentage Complete: " + str(
        (float(sts_facilities_processed_count) / float(sts_all_facilities_count)) * 100) + "%")
    log("Total Facilities: " + str(sts_all_facilities_count))
    log("Facilities Proccessed: " + str(sts_facilities_processed_count))

    log("sts_facilities_with_group_facility_type_processed_count :" + str(
        sts_facilities_with_group_facility_type_count - sts_facilities_with_group_facility_type_skipped_count))
    log("sts_facilities_with_group_keph_level_processed_count :" + str(
        sts_facilities_with_group_keph_level_count - sts_facilities_with_group_keph_level_skipped_count))
    log("sts_facilities_with_group_facility_owner_processed_count :" + str(
        sts_facilities_with_group_facility_owner_count - sts_facilities_with_group_facility_owner_skipped_count))
    log("sts_facilities_with_group_regulatory_body_processed_count :" + str(
        sts_facilities_with_group_regulatory_body_count - sts_facilities_with_group_regulatory_body_skipped_count))
    log("sts_facilities_with_group_facility_owner_type_processed_count :" + str(
        sts_facilities_with_group_facility_owner_type_count - sts_facilities_with_group_facility_owner_type_skipped_count))

    log("sts_facilities_with_group_facility_type_count :" + str(sts_facilities_with_group_facility_type_count))
    log("sts_facilities_with_group_keph_level_count :" + str(sts_facilities_with_group_keph_level_count))
    log("sts_facilities_with_group_facility_owner_count :" + str(sts_facilities_with_group_facility_owner_count))
    log("sts_facilities_with_group_regulatory_body_count :" + str(sts_facilities_with_group_regulatory_body_count))
    log(
    "sts_facilities_with_group_facility_owner_type_count :" + str(sts_facilities_with_group_facility_owner_type_count))

    log("sts_facilities_with_group_facility_type_skipped_count :" + str(
        sts_facilities_with_group_facility_type_skipped_count))
    log(
    "sts_facilities_with_group_keph_level_skipped_count :" + str(sts_facilities_with_group_keph_level_skipped_count))
    log("sts_facilities_with_group_facility_owner_skipped_count :" + str(
        sts_facilities_with_group_facility_owner_skipped_count))
    log("sts_facilities_with_group_regulatory_body_skipped_count :" + str(
        sts_facilities_with_group_regulatory_body_skipped_count))
    log("sts_facilities_with_group_facility_owner_type_skipped_count :" + str(
        sts_facilities_with_group_facility_owner_type_skipped_count))


process_org_unit_groups_for_each_facility()
