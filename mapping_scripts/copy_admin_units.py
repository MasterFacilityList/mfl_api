#!/home/elon/.virtualenv/mfl_api python2.7

import datetime
from conn import myConnection


# Simple routine to run a query on a database and print the results:
def copy_counties(conn):
    cur_select = conn.cursor()

    cur_select.execute("SELECT name, code FROM common_county")

    for name, code in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_countymapping (mfl_name, mfl_code, created, updated) "+
                           " VALUES ('"+str(name)+"',"+str(code)+", '"+str(datetime.datetime.now())+"', '"+str(datetime.datetime.now())+"')")
        print ("Inserted County - "+name)
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_sub_counties(conn):
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (LOWER(cs.name), cs.county_id) cs.id AS id, cs.name AS name, cs.code AS code, cc.name AS county_name FROM common_subcounty AS cs INNER JOIN common_county AS cc ON cs.county_id = cc.id")

    for _id, name, code, county_name in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        county_name = str(county_name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_subcountymapping (sub_county_id, mfl_name, mfl_code, county_name, created, updated) "+
                           " VALUES ('"+str(_id)+"', '"+str(name)+"',"+str(code)+", '"+str(county_name)+"', '"+str(datetime.datetime.now())+"', '"+str(datetime.datetime.now())+"')")
        print ("Inserted Sub County - "+name)
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_constituencies(conn):
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (LOWER(cs.name), cs.county_id) cs.id AS id, cs.name AS name, cs.code AS code, cc.name AS county_name FROM common_constituency AS cs INNER JOIN common_county AS cc ON cs.county_id = cc.id")

    for _id, name, code, county_name in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        county_name = str(county_name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_constituencymapping (constituency_id, mfl_name, mfl_code, county_name, created, updated) "+
                           " VALUES ('"+str(_id)+"', '"+str(name)+"',"+str(code)+", '"+str(county_name)+"', '"+str(datetime.datetime.now())+"', '"+str(datetime.datetime.now())+"')")
        print ("Inserted Constituency - "+name)
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_wards(conn):
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (LOWER(cs.name), cs.sub_county_id) cs.id AS id, cs.name AS name, cs.code AS code, cc.name AS subcounty_name FROM common_ward AS cs INNER JOIN common_subcounty AS cc ON cs.sub_county_id = cc.id")

    for _id, name, code, subcounty_name in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        subcounty_name = str(subcounty_name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_wardmapping (ward_id, mfl_name, mfl_code, sub_county_name, created, updated) "+
                           " VALUES ('"+str(_id)+"', '"+str(name)+"',"+str(code)+", '"+str(subcounty_name)+"', '"+str(datetime.datetime.now())+"', '"+str(datetime.datetime.now())+"')")
        print ("Inserted Ward - "+name)
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


def copy_facilities(conn):
    cur_select = conn.cursor()

    cur_select.execute("SELECT DISTINCT ON (LOWER(cs.name), cs.ward_id) cs.id AS id, cs.name AS name, cs.code AS code, cc.name AS ward_name FROM facilities_facility AS cs INNER JOIN common_ward AS cc ON cs.ward_id = cc.id")

    for _id, name, code, ward_name in cur_select.fetchall():
        cur_insert = conn.cursor()
        name = str(name).replace("'", "''")
        ward_name = str(ward_name).replace("'", "''")
        cur_insert.execute("INSERT INTO common_facilitymapping (facility_id, mfl_name, mfl_code, ward_name, created, updated) "+
                           " VALUES ('"+str(_id)+"', '"+str(name)+"',"+str(code)+", '"+str(ward_name)+"', '"+str(datetime.datetime.now())+"', '"+str(datetime.datetime.now())+"')")
        print ("Inserted Facility - "+name)
        # print(str(cur_insert), str(cur_select))
        conn.commit()
        cur_insert.close()

    cur_select.close()


# copy_counties(myConnection)
# copy_sub_counties(myConnection)
# copy_constituencies(myConnection)
# copy_wards(myConnection)
copy_facilities(myConnection)
myConnection.close()
