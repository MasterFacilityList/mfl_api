import psycopg2
import psycopg2.extras
added_facilities = []
failed_facilities = []
facility_services = []
added_approval = []
# conn = psycopg2.connect("")
mfl_facilities = raw_input("Please Enter comma spaced list of facilities MFL codes: \n").split(',')
dict_data = {}
service_data = {}
approval_data = {}


def push_facilities(mfl_facilities):
    try:
        conn = psycopg2.connect("dbname='mfl_old' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to the database MFL"
    try:
        conn2 = psycopg2.connect("dbname='mfl' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to databae 2 MFL_LIVE"
    cur = conn.cursor()
    cur.execute("""SELECT * FROM facilities_facility WHERE code = %s""" % mfl_code)
    rows = cur.fetchall()
    if len(rows) > 0:
        column_names = [desc[0] for desc in cur.description]
        data = zip(column_names, rows[0])
        dict_data.update(dict(data))
        print dict(data)
    else:
        print '%s is not found on db on mfl' % mfl_code

    cur2 = conn2.cursor()
    print 'db mfl_live connected'
    print dict_data
    try:
        cur2.execute(
        "INSERT INTO facilities_facility(id, created, updated, deleted, active, search, name, official_name, code, "
        "registration_number, abbreviation, description, number_of_beds, number_of_cots, open_whole_day, "
        "open_public_holidays, open_weekends, open_late_night, is_classified, is_published, attributes, "
        "regulated, approved, rejected, has_edits, bank_name,branch_name, bank_account, facility_catchment_population, "
        "nearest_landmark, plot_number, location_desc, closed, closed_date, closing_reason, created_by_id, "
        "facility_type_id, keph_level_id, operation_status_id, owner_id, parent_id, regulatory_body_id, sub_county_id, "
        "town_id, updated_by_id, ward_id, date_established, open_normal_day, license_number, regulation_status_id, "
        "town_name, county_id) VALUES (%(id)s, %(created)s, %(updated)s, %(deleted)s, %(active)s, %(search)s, "
        "%(name)s, %(official_name)s, %(code)s, %(registration_number)s, %(abbreviation)s, %(description)s, "
        "%(number_of_beds)s, %(number_of_cots)s, %(open_whole_day)s, %(open_public_holidays)s, %(open_weekends)s, "
        "%(open_late_night)s, %(is_classified)s, %(is_published)s, %(attributes)s, %(regulated)s, %(approved)s, "
        "%(rejected)s, %(has_edits)s, %(bank_name)s, %(branch_name)s, %(bank_account)s, %(facility_catchment_population)s, "
        "%(nearest_landmark)s, %(plot_number)s, %(location_desc)s, %(closed)s, %(closed_date)s, %(closing_reason)s, "
        "%(created_by_id)s, %(facility_type_id)s, %(keph_level_id)s, %(operation_status_id)s, %(owner_id)s, "
        "%(parent_id)s, %(regulatory_body_id)s, %(sub_county_id)s, %(town_id)s, %(updated_by_id)s, %(ward_id)s, "
        "%(date_established)s, %(open_normal_day)s, %(license_number)s, %(regulation_status_id)s, %(town_name)s, "
        "%(county_id)s)", dict_data)
        conn2.commit()
        added_facilities.append(mfl_code)
        print('Facility %s SUCCESS' % mfl_code)
        return dict_data['id']
    except Exception, e:
        failed_facilities.append(mfl_code)
        print 'ERROR: ', e
        print('Facility %s FAIL' % mfl_code)
        return 0


def push_service(id):
    try:
        conn = psycopg2.connect("dbname='mfl' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to the database MFL"
        cur = conn.cursor()
        cur.execute("SELECT * FROM facilities_service WHERE id = %s" % id)
        rows = cur.fetchall()
        if len(rows) > 0:
            column_names = [desc[0] for desc in cur.description]
            for row in rows:
                data = zip(column_names, row)
                service_data.update(dict(data))
            else:
                print '%s has no SERVICES in the database' % mfl_code
    #             Create insert for services
    # try:
    #     conn2 = psycopg2.connect("dbname='mfl_live' user='steve' host='localhost' password='0012'")
    #     cur2 = conn2.cursor()
    #     print 'db mfl_live SERVICES connected'
    #     print service_data
    #     try:
    #         cur2.execute(
    #             "INSERT INTO facilities_facility(id, created, updated, deleted, active, search, name, official_name, code, "
    #             "registration_number, abbreviation, description, number_of_beds, number_of_cots, open_whole_day, "
    #             "open_public_holidays, open_weekends, open_late_night, is_classified, is_published, attributes, "
    #             "regulated, approved, rejected, has_edits, bank_name,branch_name, bank_account, facility_catchment_population, "
    #             "nearest_landmark, plot_number, location_desc, closed, closed_date, closing_reason, created_by_id, "
    #             "facility_type_id, keph_level_id, operation_status_id, owner_id, parent_id, regulatory_body_id, sub_county_id, "
    #             "town_id, updated_by_id, ward_id, date_established, open_normal_day, license_number, regulation_status_id, "
    #             "town_name, county_id) VALUES (%(id)s, %(created)s, %(updated)s, %(deleted)s, %(active)s, %(search)s, "
    #             "%(name)s, %(official_name)s, %(code)s, %(registration_number)s, %(abbreviation)s, %(description)s, "
    #             "%(number_of_beds)s, %(number_of_cots)s, %(open_whole_day)s, %(open_public_holidays)s, %(open_weekends)s, "
    #             "%(open_late_night)s, %(is_classified)s, %(is_published)s, %(attributes)s, %(regulated)s, %(approved)s, "
    #             "%(rejected)s, %(has_edits)s, %(bank_name)s, %(branch_name)s, %(bank_account)s, %(facility_catchment_population)s, "
    #             "%(nearest_landmark)s, %(plot_number)s, %(location_desc)s, %(closed)s, %(closed_date)s, %(closing_reason)s, "
    #             "%(created_by_id)s, %(facility_type_id)s, %(keph_level_id)s, %(operation_status_id)s, %(owner_id)s, "
    #             "%(parent_id)s, %(regulatory_body_id)s, %(sub_county_id)s, %(town_id)s, %(updated_by_id)s, %(ward_id)s, "
    #             "%(date_established)s, %(open_normal_day)s, %(license_number)s, %(regulation_status_id)s, %(town_name)s, "
    #             "%(county_id)s)", dict_data)
    #         conn2.commit()
    # except:
    #     print "I am unable to connect to databae 2 MFL_LIVE"


def push_approval(id):
    try:
        conn = psycopg2.connect("dbname='mfl_old' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to the database MFL"
    try:
        conn2 = psycopg2.connect("dbname='mfl' user='steve' host='localhost' password='0012'")
    except:
        print "I am unable to connect to databae 2 MFL_LIVE"
    cur = conn.cursor()
    cur.execute("""SELECT * FROM facilities_facilityapproval WHERE facility_id = '%s'""" % id)
    rows = cur.fetchall()
    if len(rows) > 0:
        column_names = [desc[0] for desc in cur.description]
        data = zip(column_names, rows[0])
        approval_data.update(dict(data))
        print dict(data)
    else:
        print '%s is not found on db on mfl FACILITY APPROVAL' % mfl_code

    cur2 = conn2.cursor()
    print 'db mfl_live connected: FACILITY APPROVAL'
    print approval_data
    try:
        cur2.execute(
            "INSERT INTO facilities_facilityapproval (id, created, updated, deleted, active, search, comment, "
            "is_cancelled, created_by_id, facility_id, updated_by_id) VALUES ("
            "%(id)s, %(created)s, %(updated)s, %(deleted)s, %(active)s, %(search)s, %(comment)s, %(is_cancelled)s, "
            "%(created_by_id)s, %(facility_id)s, %(updated_by_id)s)", approval_data)
        conn2.commit()
        added_approval.append(mfl_code)
        print('Facility APPROVAL  %s SUCCESS' % mfl_code)
    except Exception, e:
        failed_facilities.append(mfl_code)
        print 'ERROR: ', e
        print('Facility APPROVAL %s FAIL' % mfl_code)


for mfl_code in mfl_facilities:
    id = push_facilities(mfl_facilities)
    if id:
        # push_service(id)
        push_approval(id)
# Add function to add related items. id returns the id of facility.


print 'Facilities Failed', failed_facilities
print 'Facilities Added', added_facilities
print 'Facilities APPROVAL', added_approval
