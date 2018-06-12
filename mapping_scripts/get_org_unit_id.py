#!/home/elon/.virtualenv/mfl_api python2.7

import requests
import base64
import json


from conn import myConnection

url = "http://localhost:8080/api/organisationUnits/"
cred = base64.b64encode("admin:district")


def get_org_unit_ids(name, level=2, filter='eq', ward_name = ""):
    print ("Mapping " + name + " :: " + ward_name)
    r = requests.get(
        url,
        headers={
            "Authorization": "Basic "+cred,
            "Accept": "application/json"
        },
        params={
            "filter": "name:"+filter+":"+name,
            "fields": "[name,id,parent]",
            "paging": "false",
            "level":level
        }
    )
    # print("Get Org Unit ID Response", r.json())
    # print("Raw Response: "+str(r.json()))
    # print(r.url)
    # print(str(r.status_code))

    res = r.json()['organisationUnits']

    if len (res) < 1:
        return False

    else:
        if len(res) == 1:
            response = {
                "dhis_name": str(res[0]["name"]),
                "dhis_id": str(res[0]["id"]),
                "dhis_parent" : str (res[0]['parent']['id'])
            }
            return response
        else:
            choices = [False] + res
            for i in range (1, len (choices)):
                print ("{} :: uid = {}\tparent = {}\tname = {}\n " .format (str(i), choices[i]['id'], choices[i]['parent']['id'], choices[i]['name']))

            while True:
                try:
                    choice = int(input ("Choice (0 to Ignore) : "))
                    break
                except SyntaxError:
                    print ("Wrong Choice")
            if choice < 1 or choice > len (choices):
                return False
            else:
                return {
                    "dhis_name": str(choices[choice]["name"]),
                    "dhis_id": str(choices[choice]["id"]),
                    "dhis_parent": str(choices[choice]['parent']['id'])
                }
# HfVjCurKxh2

# correct the county names
def correct_county_names(conn):
    tharaka = "UPDATE common_countymapping SET mfl_name = 'THARAKA NITHI' WHERE mfl_name LIKE '%THARAKA%'"
    muranga = "UPDATE common_countymapping SET mfl_name = 'MURANGA' WHERE mfl_name LIKE 'MURANG%'"
    trans = "UPDATE common_countymapping SET mfl_name = 'TRANS-NZOIA' WHERE mfl_name LIKE 'TRANS%'"
    elgeyo = "UPDATE common_countymapping SET mfl_name = 'ELGEYO-MARAKWET' WHERE mfl_name LIKE 'ELEGEYO%'"
    queries = [tharaka, muranga, trans, elgeyo]

    count = 3
    for query in queries:
        cur_update = conn.cursor()
        cur_update.execute(query)
        conn.commit()
        print ("Rem : " + str (count))
        count -= 1


def update_counties(conn):

    """

    :param conn:
    :return:

    *TODO:
    Update mfl_name of the following:

    THARAKA-NITHI , id 414 TO THARAKA NITHI
    MURANG'A , id 422 TO MURANGA
    TRANS NZOIA , id  427 TO TRANS-NZOIA
    ELEGEYO-MARAKWET id,  429 TO ELGEYO-MARAKWET


    """

    kenya_id = 'HfVjCurKxh2'
    cur_select = conn.cursor()

    cur_select.execute("SELECT id, mfl_name FROM common_countymapping")

    for id, name in cur_select.fetchall():

        name=str(name).lower()+" County"
        name = name.title()

        print("Processing "+name+"...")

        response = get_org_unit_ids(name, 2)
        cur_update = conn.cursor()
        cur_update.execute("UPDATE common_countymapping SET "+
                                  "dhis_name = '"+str(response["dhis_name"].replace ("'", "''"))+"', "+
                                  "dhis_id = '"+str(response["dhis_id"])+"', "+
                                  "dhis_parent_id = '" +kenya_id+ "'" +
                                  "WHERE id = '"+str(id)+"'")
        conn.commit()
        print("Updated "+name+"\n\n_________________________\n\n")
        cur_update.close()

    cur_select.close()
    print("Done.")


'''
Fetch all sub-counties from local mapping table and get their org unit IDs and DHIS2 name from DHIS2
-- Two occurences of Awendo sub county in MFL, I have ignored the one with MFL code 3125
-- Two occurences of Banisa (One Banisa and the other Banissa) sub county in MFL, I have ignored the one with MFL code 3125
'''

def update_subcounties (conn):
    """

    :param conn:
    :return:

    """

    cur_select = conn.cursor()
    cur_select.execute ("SELECT id, mfl_name, mfl_code FROM common_subcountymapping WHERE mfl_name > 'Ugunja' ORDER BY mfl_name ")
    # cur_select.execute("SELECT id, mfl_name, mfl_code FROM common_subcountymapping WHERE id = '582'")
    ignored = []
    for id, name, code in cur_select.fetchall():
        name = name.strip()
        name_excludes = ['sub', 'county', 'Sub', 'County ']
        name = str (' '.join ([x for x in name.split(' ') if not x in name_excludes]))
        name = str(name).lower() + " Sub County"
        name = name.title()

        print("Processing " + name + "...")
        response = get_org_unit_ids(name, 3)
        # print ("Response " + str (response))
        # if not response:
        #     ignored.append ([id, name, code])
        #     print ("Ignoring " + name)
        # else:
        cur_update = conn.cursor()
        query = "UPDATE common_subcountymapping SET dhis_name = '"+str(response["dhis_name"].replace ("'", "''"))+"', dhis_id = '"+str(response['dhis_id'])+"', dhis_parent_id = '"+ str (response['dhis_parent'] )+"'  WHERE id = '"+str(id)+"'"
        cur_update.execute(query)
        print ("Updating " + str (name) + " ...")
        conn.commit()

        ignored_file = open("ignored.json", "w")
        ignoredstr = json.dumps(ignored)
        ignored_file.write (ignoredstr)

        print ("\n\n----------------\n\n")

"""
Correct the subcounties
"""

def correct_subcounties (conn):
    sc = json.loads (open ("ignored.json").read())
    print ("\n-------------------\nTrying to correct {} Subcounties\n".format(len(sc)))

    name_excludes = ['sub', 'county', 'Sub', 'County']
    names_to_correct = [[subcounty[0], str (' '.join ([x for x in subcounty[1].split(' ') if not x in name_excludes]).strip())] for subcounty in sc]

    ignored = []

    for id, subcounty in names_to_correct:
        r = get_org_unit_ids(subcounty, 3, "ilike")
        if not r:
            print ("---\nSkipping " + subcounty)
            ignored.append (subcounty)
        else:
            query = "UPDATE common_subcountymapping SET dhis_name = '" + str(
                r["dhis_name"].replace ("'", "''")) + "', dhis_id = '" + str(r['dhis_id']) + "', dhis_parent_id = '" + str(
                r['dhis_parent']) + "'  WHERE id = '" + str(id) + "'"
            print ("Updating " + subcounty)
            cur_update = conn.cursor()
            cur_update.execute(query)
            conn.commit()

    ignored_file = open("ignored_2.json", "w")
    ignoredstr = json.dumps(ignored)
    ignored_file.write(ignoredstr)
    print ("Done")

'''
Go through the 'bad' subcounties
TODO : 
    Remove Banisa from MFL, The correct one is Banissa and is already mapped
    Change Cherengany in MFL to Cherangany
    Two occurences of Chuka/ Igambang'ombe - Split the two as they are separate subcounties
    Change Kibera in MFL to Kibra
    Kisumu Central missing in DHIS2
    Change Kituicentral in MFL to Kitui Central
    Maragwa not found in DHIS2
    Change Mt. Elgon in MFL to Mt Elgon
    Change Oljorok in MFL to Oljoroorok
    Change Olkalau in MFL to Olkalou
    Change Sigowet / Soin in MFL to Sigowet/Soin
    Webuye East in DHIS2 has two spaces in between   
    
'''

def clean_mfl_subcounties (conn):
    sc = json.loads(open("ignored_2.json").read())
    print (str (len(sc)) +  " Sub counties have cleaning problems pending")

    banisa = "";
    cherangany = "UPDATE common_subcountymapping SET mfl_name = 'Cherangany' WHERE mfl_name = 'Cherengany' "
    chuka = ""
    igambangombe = ""
    kibra = "UPDATE common_subcountymapping SET mfl_name = 'Kibra' WHERE mfl_name = 'Kibera' "
    kisumu_central = ""
    kitui_central = "UPDATE common_subcountymapping SET mfl_name = 'Kitui Central' WHERE mfl_name = 'Kituicentral' "
    maragwa = ""
    mt_elgon = "UPDATE common_subcountymapping SET mfl_name = 'Mt Elgon' WHERE mfl_name = 'Mt Elgon' "
    oljoro = "UPDATE common_subcountymapping SET mfl_name = 'Oljoroorok' WHERE mfl_name = 'Oljorok' "
    olkalau = "UPDATE common_subcountymapping SET mfl_name = 'Olkalou' WHERE mfl_name = 'Olkalau' "
    sigowet = "UPDATE common_subcountymapping SET mfl_name = 'Sigowet/Soin' WHERE mfl_name = 'Sigowet / Soin' "
    webuye_east = "UPDATE common_subcountymapping SET mfl_name = 'Webuye  East' WHERE mfl_name = 'Webuye East'"

    queries = [banisa, cherangany, chuka, igambangombe, kibra, kisumu_central, kitui_central, maragwa, mt_elgon, oljoro, olkalau, sigowet, webuye_east]
    q = ""
    for query in queries:
        if len(query) > 2:
            q += query + ";\n"
            # cur_qry = conn.cursor()
            # cur_qry.execute(query)
            # conn.commit()
            # cur_qry.close()

    print (q)

#     get the subcounties that are still null
    still_null_cur = conn.cursor()
    still_null_cur.execute ("SELECT mfl_name FROM common_subcountymapping WHERE dhis_name IS NULL")


    for name in still_null_cur.fetchall():
        name = str(name).lower()
        name = name.title()



        # r = get_org_unit_ids(name, 3, "ilike")
        # if not r:
        #     print ("Unable to resolve " + name)
        # else:
        #     query = "UPDATE common_subcountymapping SET dhis_name = '" + str(
        #         r['dhis_name']) + "', dhis_id = '" + str(r['dhis_id']) + "', dhis_parent_id = '" + str(
        #         r['dhis_parent']) + "'  WHERE id = '" + str(id) + "'"
        #     print ("Updating " + name)
        #     cur_update = conn.cursor()
        #     cur_update.execute(query)
        #     conn.commit()
        #


"""
Update the Wards
"""

def update_wards (conn):
    fetch_cur = conn.cursor()
    fetch_cur.execute ("SELECT id, mfl_name, mfl_code FROM common_wardmapping WHERE dhis_name IS NULL AND mfl_name > 'MUKOGONDO WEST' ORDER BY mfl_name ASC")
    # fetch_cur.execute("SELECT id, mfl_name, mfl_code FROM common_wardmapping WHERE id =  '1465' ")
    print ("We have {} Wards in MFL".format(str(fetch_cur.rowcount)))
    ignored = 0

    for id, name, code in fetch_cur.fetchall():
        name = str(name).lower() + " Ward"
        name = name.title()

        r = get_org_unit_ids(name, 4, "eq")
        if r:
            cur_update = conn.cursor()
            query = "UPDATE common_wardmapping SET dhis_name = '" + str(
                r["dhis_name"].replace ("'", "''")) + "', dhis_id = '" + str(r['dhis_id']) + "', dhis_parent_id = '" + str(
                r['dhis_parent']) + "'  WHERE id = '" + str(id) + "'"
            cur_update.execute (query)
            conn.commit()
            print ("Updating " + name)

    print ("Ignored " + str (ignored))


def update_facility(conn):
    fetch_cur = conn.cursor()
    fetch_cur.execute ("SELECT id, mfl_name, mfl_code, ward_name FROM common_facilitymapping WHERE dhis_name IS NULL ORDER BY mfl_name ASC")
    # fetch_cur.execute("SELECT id, mfl_name, mfl_code, ward_name FROM common_wardmapping WHERE id =  '1465' ")
    print ("We have {} Pending Facilities in MFL\n".format(str(fetch_cur.rowcount)))
    ignored, corrected = 0, 0
    total = float(fetch_cur.rowcount)
    done = 1

    for id, name, code, ward_name in fetch_cur.fetchall():
        name = str(name).lower()
        name = name.title()
        name = name.split (" ")[0]

        r = get_org_unit_ids(name, 6, "ilike", ward_name)
        if r:

            cur_update = conn.cursor()
            query = "UPDATE common_facilitymapping SET dhis_name = '" + str(
                r["dhis_name"].replace ("'", "''")) + "', dhis_id = '" + str(r['dhis_id']) + "', dhis_parent_id = '" + str(
                r['dhis_parent']) + "'  WHERE id = '" + str(id) + "'"
            cur_update.execute (query)
            conn.commit()
            print ("Updating " + name + "\n\n")
            corrected += 1
            print ("Updated " + name + "\n")
        else:
            ignored += 1
            print ("Skipping " + name + "\n")

        perc = (float(done)/total)*100
        print ("..... {}% Done". format(str(perc)))
        done += 1

    print ("Corrected {} :: Ignored {}" .format (str(corrected), str(ignored)))

# correct_county_names(myConnection)
# update_counties(myConnection)
# update_subcounties(myConnection)
# correct_subcounties(myConnection)
'''
At this Point, stop and clean the subcounties in the ignored_2.json (better to fetch from the table where dhis_name IS NULL
'''
# clean_mfl_subcounties(myConnection)
# update_wards(myConnection)
update_facility(myConnection)




