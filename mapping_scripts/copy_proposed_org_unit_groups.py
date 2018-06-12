from conn import myConnection as conn
import datetime


def copy_facility_keph_levels():
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (name) name, id FROM facilities_kephlevel")

    for name, _id in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_orgunitgroupsmapping (mfl_name, created, updated) " +
                           " VALUES ('" + "KEPH "+str(name) + "', '" + str(
            datetime.datetime.now()) + "', '" + str(datetime.datetime.now()) + "')")
        print ("Inserted KEPH Level - " + str(name))
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_facility_owners():
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (name) name, id FROM facilities_owner")

    for name, _id in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_orgunitgroupsmapping (mfl_name, created, updated) " +
                           " VALUES ('" + str(name) + "', '" + str(
            datetime.datetime.now()) + "', '" + str(datetime.datetime.now()) + "')")
        print ("Inserted Facility Owner - " + str(name))
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_facility_owner_type():
    cur_select = conn.cursor()

    cur_select.execute("SELECT name, id FROM facilities_ownertype")

    for name, _id in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_orgunitgroupsmapping (mfl_name, created, updated) " +
                           " VALUES ('" + str(name) + "', '" + str(
            datetime.datetime.now()) + "', '" + str(datetime.datetime.now()) + "')")
        print ("Inserted Facility Owner Type - " + str(name))
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_facility_regulating_body():
    cur_select = conn.cursor()

    cur_select.execute("SELECT name, id FROM facilities_regulatingbody")

    for name, _id in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_orgunitgroupsmapping (mfl_name, created, updated) " +
                           " VALUES ('" + str(name) + "', '" + str(
            datetime.datetime.now()) + "', '" + str(datetime.datetime.now()) + "')")
        print ("Inserted Facility Regulating Body - " + str(name))
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_facility_type():
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (sub_division) sub_division, id FROM facilities_facilitytype WHERE sub_division IS NOT NULL")

    for sub_division, _id in cur_select.fetchall():
        cur_insert = conn.cursor()
        sub_division = str(sub_division).replace("'", "''")
        cur_insert.execute("INSERT INTO common_orgunitgroupsmapping (mfl_name, created, updated) " +
                           " VALUES ('" + str(sub_division) + "', '" + str(
            datetime.datetime.now()) + "', '" + str(datetime.datetime.now()) + "')")
        print ("Inserted Facility Type - " + str(sub_division))
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_facility_type_details():
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (name) name, id FROM facilities_facilitytype WHERE sub_division IS NOT NULL")

    for name, _id in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_orgunitgroupsmapping (mfl_name, created, updated) " +
                           " VALUES ('" + str(name) + "', '" + str(
            datetime.datetime.now()) + "', '" + str(datetime.datetime.now()) + "')")
        print ("Inserted Facility Type Details - " + str(name))
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


copy_facility_owner_type()
copy_facility_regulating_body()
copy_facility_type()
copy_facility_type_details()
copy_facility_owners()
copy_facility_keph_levels()
