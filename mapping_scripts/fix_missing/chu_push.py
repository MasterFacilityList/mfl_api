import psycopg2
import psycopg2.extras
import json

'''
added_facilities = []
failed_facilities = []
facility_services = []
added_approval = []
dict_data = {}
service_data = {}
approval_data = {}
'''

statistics = {}
chu_data = {}


def setup_stats(chu_codes=[]):
    statistics.update({
        "detailed": {
            chu_code:{} for chu_code in chu_codes 
        },
        "summary": {
            "added_chus": [],
            "failed_chus": [],
            "approved_chus": [],
            "added_services": [],
            "not_found": [],
            "za_added_chus_count": 0,
            "zb_failed_chus_count": 0,
            "zc_approved_chus_count": 0,
            "zd_added_services_count": 0,
            "ze_not_found_count": 0,
            "zz_total_count": len(chu_codes)
        }
    })


def record_stats(chu_code=0, found=False, added=False, approved=False, meta={}):
    if chu_code in statistics["detailed"]:
        statistics["detailed"][chu_code].update({
            "found": found,
            "added": added,
            "approved": approved,
            "meta": meta,
            "services": []
        })
        if not found: statistics["summary"]["not_found"].append(chu_code)
        if added: statistics["summary"]["added_chus"].append(chu_code)
        if not added: statistics["summary"]["failed_chus"].append(chu_code)
        if approved: statistics["summary"]["approved_chus"].append(chu_code)
        statistics["summary"]["za_added_chus_count"] = len(statistics["summary"]["added_chus"])
        statistics["summary"]["zb_failed_chus_count"] = len(statistics["summary"]["failed_chus"])
        statistics["summary"]["zc_approved_chus_count"] = len(statistics["summary"]["approved_chus"])
        statistics["summary"]["ze_not_found_count"] = len(statistics["summary"]["not_found"])


def record_service_stats(chu_code=0, added_services=False, services=[]):
    if chu_code in statistics["detailed"]:
        statistics["detailed"][chu_code]["services"] = services
        if added_services: statistics["summary"]["added_services"].append(chu_code)
        statistics["summary"]["zd_added_services_count"] = len(statistics["summary"]["added_services"])


def log(stats={}):
    with open("logs.json", 'w') as logs:
        logs.write(json.dumps(stats, sort_keys=True, indent=4))
        logs.close()


def update_chu_meta(chu_id):
    try:
        conn = psycopg2.connect("dbname='mfl_old' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to the database MFL_OLD"

    cur = conn.cursor()
    cur.execute("""SELECT
         chu.id AS chu_id,
         chu.code AS chu_code,
         chu.name AS chu_name,
         chu.is_approved AS chu_is_approved,
         f.name AS facility_name,
         cw.name AS ward_name,
         cc.name AS constituency_name,
         cs.name AS sub_county_name,
         cct.name AS county_name
         FROM chul_communityhealthunit AS chu
         LEFT JOIN facilities_facility AS f ON f.id = chu.facility_id
         LEFT JOIN common_ward AS cw ON cw.id = f.ward_id
         LEFT JOIN common_constituency AS cc ON cc.id  = cw.constituency_id
         LEFT JOIN common_subcounty AS cs ON cs.id  = cw.sub_county_id
         LEFT JOIN common_county AS cct ON cct.id = cc.county_id
         WHERE chu.id = '%s'""" % chu_id)
    try:
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        meta = dict(zip(column_names, rows[0]))
        record_stats(str(meta["chu_code"]), True, True, meta["chu_is_approved"], meta)
        return {"id": meta["chu_id"], "code": meta["chu_code"]}
    except Exception, e:
        return {"id": "00000000-0000-0000-0000-000000000000", "code": 0}
        print 'ERROR: ', e


def push_chu_services(chu):
    try:
        conn = psycopg2.connect("dbname='mfl_old' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to the database MFL_OLD"
    try:
        conn2 = psycopg2.connect("dbname='mfl' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to database MFL_NEW"
    cur = conn.cursor()
    cur.execute("""SELECT * FROM chul_chuservicelink WHERE health_unit_id = '%s'""" % chu["id"])
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    services = []

    if len(rows) > 0:
        record_service_stats(chu["code"], True)
    else:
        record_service_stats(str(chu["code"]))

    for row in rows:
        service = dict(zip(column_names, row))
        cur2 = conn2.cursor()
        try:
            cur2.execute(
            """INSERT INTO public.chul_chuservicelink (
                id,created,updated,deleted,active,
                search,health_unit_id,created_by_id,
                service_id,updated_by_id)
                VALUES (
                %(id)s,%(created)s,%(updated)s,
                %(deleted)s,%(active)s,%(search)s,
                %(health_unit_id)s,%(created_by_id)s,
                %(service_id)s,%(updated_by_id)s)""", service)
            conn2.commit()
            
        except Exception, e:
            record_service_stats(chu["code"])
            print 'ERROR: ', e

        cur.execute("""SELECT name FROM chul_chuservice WHERE id = '%s'""" % service["service_id"])
        services.append(dict(zip([desc[0] for desc in cur.description], cur.fetchall()[0]))["name"])

    record_service_stats(str(chu["code"]), False, services)


def push_chu(chu_code):
    try:
        conn = psycopg2.connect("dbname='mfl_old' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to the database MFL_OLD"
    try:
        conn2 = psycopg2.connect("dbname='mfl' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to database MFL_NEW"
    cur = conn.cursor()
    rows = None
    try:
        cur.execute("""SELECT * FROM chul_communityhealthunit WHERE code = %s""" % chu_code)
        rows = cur.fetchall()
    except Exception, e:
        record_stats(chu_code)
        print 'ERROR: ', e
        return "00000000-0000-0000-0000-000000000000"

    if len(rows) > 0:
        column_names = [desc[0] for desc in cur.description]
        chu_data.update(dict(zip(column_names, rows[0])))       
    else:
        record_stats(chu_code)
    
    cur2 = conn2.cursor()
    try:
        cur2.execute(
        """INSERT INTO public.chul_communityhealthunit
        (id,created,updated,deleted,active,search,name,code,households_monitored,
        date_established,date_operational,is_approved,approval_comment,approval_date,
        location,is_closed,closing_comment,is_rejected,rejection_reason,has_edits,
        created_by_id,facility_id,status_id,updated_by_id,number_of_chvs)
        VALUES
        (%(id)s,%(created)s,%(updated)s,%(deleted)s,%(active)s,%(search)s,
        %(name)s,%(code)s,%(households_monitored)s,%(date_established)s,
        %(date_operational)s,%(is_approved)s,%(approval_comment)s,%(approval_date)s,
        %(location)s,%(is_closed)s,%(closing_comment)s,%(is_rejected)s,%(rejection_reason)s,
        %(has_edits)s,%(created_by_id)s,%(facility_id)s,%(status_id)s,%(updated_by_id)s,
        %(number_of_chvs)s)""", chu_data)
        conn2.commit()
        record_stats(chu_code, True, True, chu_data["is_approved"])
        return chu_data['id']
    except Exception, e:
        record_stats(chu_code, True, False)
        print 'ERROR: ', e
        return "00000000-0000-0000-0000-000000000000"

# conn = psycopg2.connect("")

input_mode = raw_input("Provide comma separated list of CHU codes. \n\
Prefered mode: Console [c] / File [f]: ").strip()

if input_mode == 'c':
    chu_codes = raw_input("Paste list: \n").split(',')
    setup_stats(chu_codes)
    for chu_code in chu_codes:
        push_chu(chu_code)

elif input_mode == 'f':
    chu_codes_file_path = raw_input("Provide full path to file (Single line with no \\n): \n").strip()
    chu_codes = []
    with open(chu_codes_file_path, 'r') as file:
        chu_codes = file.read().replace('\n', '').split(',')
        file.close()
    
    setup_stats(chu_codes)
    for chu_code in chu_codes:
        update_chu_meta(push_chu(chu_code))
else:
    print "Unknown Option!"

log(statistics)