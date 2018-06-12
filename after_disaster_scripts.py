from chul.models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthUnitContact,
    CHUServiceLink
)
from common.models import Contact
from users.models import MflUser
from facilities.models import (
    Facility, FacilityService, FacilityOfficer, Officer, OfficerContact,
    FacilityContact, FacilityUnit, FacilityRegulationStatus,
    FacilityApproval)
from mfl_gis.models import FacilityCoordinates

user = MflUser.objects.get(email='system@ehealth.or.ke')


def delete_the_created_chuls():
    chuls = CommunityHealthUnit.objects.filter(code__gte=700000)
    for chu in chuls:
        chew = CommunityHealthWorker.objects.filter(health_unit=chu)
        chew.delete()
        contacts = CommunityHealthUnitContact.objects.filter(health_unit=chu)
        for con in contacts:
            con_objs = Contact.objects.filter(contact=con.contact)
            for con_obj in con_objs:
                con_obj.delete()
                con.delete()

        services = CHUServiceLink.objects.filter(health_unit=chu)
        for service in services:
            service.delete()
        chu.delete()


from xlrd import open_workbook
from common.models import County, SubCounty, Constituency, Ward

import json


def read_ward_sub_counties_excel_file(file_path=None, write_file=None):
    if not file_path:
        file_path = 'wards_and_sub_counties.xlsx'
    wb = open_workbook(file_path)

    values = []
    append = values.append

    for sheet in wb.sheets():
        n_of_rows = sheet.nrows

        for row in xrange(1, n_of_rows):
            data = {
                "county": sheet.cell(row, 0).value,
                "constituency": sheet.cell(row, 1).value,
                "ward": sheet.cell(row, 2).value,
                "sub_county": sheet.cell(row, 3).value
            }

            append(data)
    if not write_file:
        write_file = 'wards_and_sub_counties.json'

    with open(write_file, 'w+') as data_file:
        json.dump(values, data_file, indent=4)


def load_wards_and_sub_counties_json_file():
    with open('wards_and_sub_counties.json') as data_file:
        data = data_file.read()
        data = json.loads(data)
        for record in data:
            county_name = record.get('county')
            ward_name = record.get('ward')
            sub_county_name = record.get('sub_county')
            constituency_name = record.get('constituency')
            try:
                county_obj = County.objects.get(name__contains=county_name)
            except:
                import pdb
                pdb.set_trace()
            try:
                constituency_obj = Constituency.objects.get(
                    name=constituency_name, county=county_obj)
            except:
                import pdb
                pdb.set_trace()
            try:
                sub = SubCounty.objects.get(
                    name=sub_county_name.lower(), county=county_obj)
            except:
                print "created sub county {}".format(sub_county_name)
                sub = SubCounty.objects.create(
                    name=sub_county_name.lower(), county=county_obj,
                    created_by=user, updated_by=user)

            try:
                ward = Ward.objects.get(
                    name=ward_name, constituency=constituency_obj,
                    constituency__county=county_obj)
                ward.sub_county = sub
                ward.save()
                print "{} ==>{} ==>{} ==>{}".format(
                    county_name, constituency_name,
                    sub_county_name, ward_name)
            except:
                import pdb
                pdb.set_trace()


def delete_unwanted_facilities():
    facilities = Facility.objects.filter(code__gte=50000)
    for facility in facilities:
        # delete facility services
        for fs in FacilityService.objects.filter(facility=facility):
            fs.delete()

        # delete facility coords
        try:
            FacilityCoordinates.objects.get(facility=facility).delete()
        except:
            pass

        # delete facility contacts
        for fc in FacilityContact.everything.filter(facility=facility):
            for con in Contact.objects.filter(contact=fc.contact):
                con.delete()
            import pdb
            pdb.set_trace()
            fc.delete()

        for unit in FacilityUnit.objects.filter(facility=facility):
            unit.delete()

        for fo in FacilityOfficer.objects.filter(facility=facility):
            officer = Officer.objects.get(id=fo.officer.id)
            for officer_contact in OfficerContact.objects.filter(
                    officer=officer):
                for con in Contact.objects.filter(
                        contact=officer_contact.contact):
                    con.delete()
            officer_contact.delete()
            fo.delete()

        for reg_status in FacilityRegulationStatus.objects.filter(facility=facility):
            reg_status.delete()

        for approval in FacilityApproval.objects.filter(facility=facility):
            approval.delete()

        print facility.id
        facility.delete()
