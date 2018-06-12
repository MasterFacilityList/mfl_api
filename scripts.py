import json

from facilities.models import Facility
from common.models import County, Ward


def fix_date_established():
    bad_date = Facility.objects.all()[1].date_established
    for fac in Facility.objects.filter(date_established=bad_date):
        fac.date_established = None
        fac.save(allow_save=True)


def fix_town_name():
    for fac in Facility.objects.all():
        if fac.town:
            fac.town_name = fac.town.name
        try:
            fac.save(allow_save=True)
        except:
            print "unable to update town"


# from xlrd import open_workbook

# def read_facilities_with_wards_file(file_path=None, write_file=None):
#     if not file_path:
#         file_path = 'facitlities_with_wards.xlsx'
#     wb = open_workbook(file_path)

#     values = []
#     append = values.append

#     for sheet in wb.sheets():
#         n_of_rows = sheet.nrows

#         for row in xrange(1, n_of_rows):
#             data = {
#                 "facility_code": sheet.cell(row, 0).value,
#                 "county": sheet.cell(row, 1).value,
#                 "ward": sheet.cell(row, 2).value
#             }

#             append(data)
#     if not write_file:
#         write_file = 'faciltiy_with_wards_json.json'

#     with open(write_file, 'w+') as data_file:
#         json.dump(values, data_file, indent=4)


def move_facitlies_to_correct_ward(file_path=None):
    if not file_path:
        file_path = 'misplaced_facilities.json'
    with open(file_path) as data_file:
        data = json.loads(data_file.read())
        for record in data:
            try:
                fac = Facility.objects.get(code=int(record.get('facility_code')))
            except Facility.DoesNotExist:
                print "facility not found"
                continue

            if record.get('county'):
                county_name = record.get('county').split()[0]

            if county_name == 'Elgeyo':
                county_name = 'Elegeyo'

            try:
                county = County.objects.filter(name__icontains=county_name)[0]
            except IndexError:
                import pdb; pdb.set_trace()

            prob_ward = Ward.objects.filter(constituency__county=county)
            try:
                ward = prob_ward.filter(name__icontains=record.get('ward'))[0]
            except IndexError:
                import pdb
                pdb.set_trace()
            fac.ward = ward
            print county, ward
            try:
                fac.save(allow_save=True)
            except:
                import pdb
                pdb.set_trace()


def determine_facilites_already_in_system():
    file_path = 'new_missing_facilities.json'
    with open(file_path) as data_file:
        data = json.loads(data_file.read())
        codes = []
        for record in data:
            try:
                Facility.objects.get(code=int(record.get('facility_code')))
            except Facility.DoesNotExist:
                codes.append(record.get('facility_code'))
                print "facility not found"
                continue
        with open('missing_but_in_system', 'w+') as data_file:
            json.dump(codes, data_file, indent=4)
