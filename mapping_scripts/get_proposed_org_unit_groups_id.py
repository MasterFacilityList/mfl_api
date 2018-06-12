import requests
import base64
import json

from conn import myConnection as conn

url = "http://test.hiskenya.org/dev/api/organisationUnitGroups"
cred = base64.b64encode("healthit:hEALTHIT2017")


def get_org_unit_group_ids(payload):
    r = requests.get(
        url,
        headers={
            "Authorization": "Basic "+cred,
            "Accept": "application/json"
        },
        params={
            "filter": "name:eq:"+payload,
            "fields": "[name,id,code,groupSets]",
            "paging": "false",
        }
    )
    # print("Get Org Unit ID Response", r.json())
    raw_response = r.json()["organisationUnitGroups"][0]
    print("Raw Response: "+str(raw_response))

    return {
        "dhis_id": raw_response["id"],
        "dhis_name": raw_response["name"],
        "group_code": raw_response["code"],
        "group_set_ids": raw_response["groupSets"]
    }


def update_groups(conn):
    cur_select = conn.cursor()

    cur_select.execute("SELECT id, mfl_name FROM common_orgunitgroupsmapping")

    for id, mfl_name in cur_select.fetchall():
        mfl_name = "MFL-"+mfl_name
        print("Processing "+mfl_name+"...")

        response = get_org_unit_group_ids(mfl_name)
        cur_update = conn.cursor()
        cur_update.execute("UPDATE common_orgunitgroupsmapping SET "+
                                  "dhis_name = '"+str(response["dhis_name"].replace ("'", "''"))+"', "+
                                  "dhis_id = '"+str(response["dhis_id"])+"', "
                                  "group_set_ids = '"+str(response["group_set_ids"]).replace("'", "''")+"', "
                                  "group_code = '" +str(response["group_code"])+ "' " +
                                  "WHERE id = '"+str(id)+"'")
        conn.commit()
        print("Updated "+mfl_name+"\n\n_________________________\n\n")
        cur_update.close()

    cur_select.close()
    print("Done.")



update_groups(conn)

