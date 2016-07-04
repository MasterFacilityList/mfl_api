import json
import pytz

from dateutil import parser
from django.utils import timezone

from facilities.models import Facility, Owner, RegulatingBody, FacilityType, FacilityStatus, KephLevel
from users.models import MflUser
from common.models import County, Ward


user = MflUser.objects.get(email='system@ehealth.or.ke')


def load_missed_facilities():
    fac_wards = open('faciltiy_with_wards_json.json')
    fac_wards_data = fac_wards.read()
    facility_wards_data = json.loads(fac_wards_data)
    facs_created  = []

    file_path = 'missed_codes_facility_records.json'
    with open(file_path) as data_file:
        data = data_file.read()
        data = json.loads(data)
        for record in data:

            try:
                Facility.objects.get(code=int(record.get('code')))
                continue

            except Facility.DoesNotExist:
                pass

            county_name = record.get('county').split()[0]

            if county_name == 'Elgeyo':
                county_name ='Elegeyo'

            try:
                county = County.objects.filter(name__icontains=county_name)[0]
            except IndexError:
                import pdb; pdb.set_trace()

            print county, record.get('county')
            reg_body = None

            if record.get('regulatory_body'):
                try:
                    reg_body = RegulatingBody.objects.get(name=record.get('regulatory_body').get('name'))
                except RegulatingBody.DoesNotExist:
                    pass

            facility_type = FacilityType.objects.get(name=record.get('facility_type').get('name'))
            try:
                owner = Owner.objects.get(name=record.get('owner').get('name'))
            except Owner.DoesNotExist:
                moh = Owner.objects.get(name='Ministry of Health')
                owner = moh
            try:
                operation_status = FacilityStatus.objects.get(name=record.get('operation_status').get('name'))
            except AttributeError:
                import pdb
                pdb.set_trace()

            facility_data = {
                "code": int(record.get('code')),
                "name": record.get('name'),
                "created": pytz.utc.localize(parser.parse(record.get('created'))),
                "owner": owner,
                "facility_type": facility_type,
                "operation_status": operation_status,
                "county": county,
                "created_by": user,
                "updated_by": user
            }

            if reg_body:
                facility_data['regulatory_body'] = reg_body

            if record.get('official_name') != '':
                facility_data['official_name'] = record.get('official_name')

            if record.get('keph_level'):
                try:
                    keph = KephLevel.objects.get(name=record.get('keph_level').get('name'))
                    facility_data['keph_level'] = keph
                except KephLevel.DoesNotExist:
                    pass

            for fac_ward in facility_wards_data:
                if int(facility_data.get('code')) == int(fac_ward.get('faciilty_code')):
                    prob_ward = Ward.objects.filter(constituency__county=county)
                    try:
                        ward = prob_ward.filter(name__icontains=fac_ward.get('ward'))[0]
                    except:
                    facility_data['ward'] = ward
                    try:
                        Facility.objects.get(code=int(record.get('code')))
                        print "facility exists"
                    except Facility.DoesNotExist:

                        try:
                            Facility(**facility_data).save()
                            facs_created.append(facility)
                            print facility
                        except:
                            pass
                            # import pdb; pdb.set_trace()
                    break

    return len(facs_created)


            # # try:
            # #     Facility(**facility_data).save()
            # # except:
            # #     import pdb; pdb.set_trace()
            # try:
            #     facility = Facility.objects.get(code=record.get('code'))
            #     facility.county = county
            #     facility.save(allow_save=True)

            # except Facility.DoesNotExist:
            #     pass




# def assign_psuedo_wards():
#     fac_wards = open('faciltiy_with_wards_json.json')
#     fac_wards_data = fac_wards.read()
#     facility_data = json.loads(fac_wards_data)

#     for facility in Facility.objects.exclude(county__isnull=True):

#         for fac_ward in facility_data:
#             if int(facility.code) == int(fac_ward.get('faciilty_code')):
#                 if facility.county:
#                     prob_ward = Ward.objects.filter(constituency__county=facility.county)
#                     ward = prob_ward.filter(name__icontains=fac_ward.get('ward'))[0]
#                     facility.ward = ward
#                     facility.save(allow_save=True)


def get_facilities_not_loaded_report():
    fac_wards = open('faciltiy_with_wards_json.json')
    fac_wards_data = fac_wards.read()
    error_facilities = []
    facility_wards_data = json.loads(fac_wards_data)
    for fac_ward in facility_wards_data:
        try:
            Facility.objects.get(code=int(fac_ward.get('faciilty_code')))
        except Facility.DoesNotExist:
            error_facilities.append(fac_ward)

    with open('facilities_not_loaded.json', 'w+') as data_file:
        json.dump(error_facilities, data_file, indent=4)

    return len(error_facilities)


from facilities.models import Facility, FacilityType

def map_facility_types():
    facility_types_map = {
        "Stand Alone": None,
        "VCT Centre (Stand-Alone)": "VCT",
        "Training Institution in Health (Stand-alone)": None,
        "Sub-District Hospital": "Primary care hospitals",
        "Rural Health Training Centre": "Comprehensive primary health care facility",
        "Rural Health Demonstration Centre": "Comprehensive primary health care facility",
        "Regional Blood Transfusion Centre": "Regional Blood Transfusion Centre",
        "Radiology Unit": "Radiology Clinic",
        "County Referral Hospitals": "Comprehensive Teaching &Referral",
        "Other Hospital": "Primary care hospitals",
        "Other": None,
        "Nursing Home": "Basic primary health care facility",
        "Not in List": "Basic primary health care facility",
        "National Teaching & Tertiary Referral Hospitals": "Comprehensive Teaching &Referral",
        "Medical Clinic": "Dispensaries and clinic-out patient only",
        "Medical Centre": "Dispensaries and clinic-out patient only",
        "Maternity Home": "Basic primary health care facility",
        "Maternity and Nursing Home": "Basic primary health care facility",
        "Laboratory (Stand-alone)": "Laboratory",
        "Hospital": None,
        "Funeral Home (Stand-alone)": "Farewell Home",
        "Eye Clinic": "Dispensaries and clinic-out patient only",
        "Eye Centre": "Basic primary health care facility",
        "Eye": "Basic primary health care facility",
        "District Hospital": "Secondary care hospitals",
        "Dispensary": "Dispensaries and clinic-out patient only",
        "Dental Clinic": "Dispensaries and clinic-out patient only",
        "Blood Bank": "Blood Bank",
        "Health Centre": "Basic primary health care facility",
        "Not In List": "Dispensaries and Clinics",
        "Health Project": "Administrative Offices",
        "Health Programme": "Administrative Offices",
        "Training Institution in Health (Stand-alone)": "Administrative Offices",
        "District Health Office": "Administrative Offices"
    }
    for facility in Facility.objects.all():
        new_type = facility_types_map.get(facility.facility_type.name)
        if new_type:
            try:
                facility_type_obj = FacilityType.objects.get(name=new_type)
            except FacilityType.DoesNotExist:
                import pdb
                pdb.set_trace()
            facility.facility_type = facility_type_obj
            facility.save(allow_save=True)


"""
Health Centre
Eye Clinic ==> Moved to eye
Eye Centre ==> Moved to eye
Not In List
Training Institution in Health (Stand-alone)
Health Project
Health Programme

[f.facility_type.name for f in Facility.objects.all() if f.facility_type.name not in  facility_types_map.values()]

Ensure all stand alone have been created and assigned to the Stand Alone Parent
"""


# def update all facility types with parents with parent FK


def update_facility_types_with_parents():
    for f_type in FacilityType.objects.all():
        if f_type.sub_division:
            parent_obj = FacilityType.objects.get(name=f_type.sub_division)
            f_type.parent = parent_obj
            f_type.save()


"""
Issues
Eye
Blood bank
Health Centre
Health clinic

"""
"""
0
:
37.64954663579162
1
:
-0.446732937212727
"""


def remove_invalid_and_unknown_status():
    from facilities.models import Facility, FacilityStatus
    closed = FacilityStatus.objects.get(name='Closed')
    for facility in Facility.objects.filter(operation_status__name__in=['Invalid', 'Unknown']):
            facility.operation_status = closed
            facility.save(allow_save=True)
            print facility

def undelete_facility_types():
    from facilities.models import FacilityType
    for facility_type in FacilityType.everything.filter(deleted=True):
        facility_type.deleted = False
        try:
            facility_type.save()
        except:
            pass

def delete_facility_types():
    from facilities.models import FacilityType, Facility
    for facility_type in FacilityType.objects.all():
        if Facility.objects.filter(facility_type=facility_type).count() == 0:
            try:
                facility_type.delete()
            except:
                pass


def remove_invalid_and_unknown_status():
    from facilities.models import Facility, FacilityStatus
    from django.utils import timezone
    closed = FacilityStatus.objects.get(name='Closed')
    for facility in Facility.objects.filter(closed=False, operation_status=closed):
            facility.operation_status = closed
            facility.save(allow_save=True)
            print facility


def fix_closed_approved_facilities():
    from facilities.models import Facility, FacilityStatus
    closed_facilities = Facility.objects.filter(closed=False, operation_status__name=)
    closed_facilities = Facility.objects.filter(closed=False, has_edits=False, approved=False, rejected=True)
    # for fac in closed_facilities:
        # fac.approved = True
        # fac.has_edits = False
        # fac.save(allow_save=True)
    return [fac.name for fac in closed_facilities]

from facilities.models import Facility, FacilityApproval
def approve_facilities():
    for fac in Facility.objects.filter(approved=False, rejected=False):
        fac.approved = True
        FacilityApproval.objects.create(facility=fac, created_by=user, updated_by=user)
        fac.save(allow_save=True)
