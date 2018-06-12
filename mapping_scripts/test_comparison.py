# encoding=utf8  
import sys
import os
import time
file_path = '/home/sam/Documents/mfl.xlsx'
try:
    os.remove(file_path)
except:
    pass

reload(sys)  
sys.setdefaultencoding('utf8')
start  = int(round(time.time() * 1000))

import requests
import base64
import json
import xlsxwriter



from conn import myConnection

url = "http://localhost:8080/api/organisationUnits/"
cred = base64.b64encode("admin:district")

def orgunitname (id):
    r = requests.get (
        url + id,
        headers = {
        "Authorization": "Basic "+cred,
        "Accept": "application/json"
        },
        params = {
            "fields": "[name]",
            "paging": "false"
        }
    )
    return r.json()['name']


# fetch from DHIS2

r = requests.get(
    url,
    headers = {
        "Authorization": "Basic "+cred,
        "Accept": "application/json"
    },
    params = {
        "fields": "[name,id,parent]",
        "paging": "false",
        "level":5
    }
) 

all_facilities = r.json()['organisationUnits']

# fetch mapped facilities from common mapping table
mapped_cur = myConnection.cursor()
mapped_cur.execute ("SELECT dhis_id, dhis_name FROM common_facilitymapping WHERE dhis_name IS NOT NULL")
mapped_facilities = mapped_cur.fetchall()
mapped_ids = [id for id, name in mapped_facilities]

unmapped = [ fac for fac in all_facilities if fac['id'] not in mapped_ids]

# fetch from local mapping table
 
cur_select = myConnection.cursor()

cur_select.execute("SELECT id, mfl_name, mfl_code, ward_name, dhis_name, dhis_id FROM common_facilitymapping WHERE dhis_name IS NULL")
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()

worksheet.write ('A1', 'MFL ID')
worksheet.write ('B1', 'MFL CODE')
worksheet.write ('C1', 'MFL NAME')
worksheet.write ('D1', 'MFL PARENT')

worksheet.write ('E1', 'DHIS ID')
worksheet.write ('F1', 'DHIS NAME')
worksheet.write ('G1', 'DHIS PARENT')

worksheet.write ('H1', 'MFL_DHIS_NAME')
worksheet.write ('I1', 'MFL_DHIS_ID')
worksheet.write ('J1', 'MFL_DHIS_PARENT')


row = 2
for mfl_id, name, code, ward, dhis_name, dhis_id in cur_select.fetchall():
    
    worksheet.write ('A'+str(row), mfl_id)
    worksheet.write ('B'+str(row), code)
    worksheet.write ('C'+str(row), str(name))
    worksheet.write ('D'+str(row), str(ward))
    row += 1

row = 2

for uf in unmapped:
    worksheet.write ('E'+str(row), uf['id'])
    worksheet.write ('F'+str(row), uf['name'])
    worksheet.write ('G'+str(row), orgunitname (uf['parent']['id']))
    row += 1

workbook.close()

print ("Stop : " +  str (int(round(time.time() * 1000)) - start) + " MS")