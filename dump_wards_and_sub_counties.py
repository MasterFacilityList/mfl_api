import json

from common.models import Ward, SubCounty, County
from users.models import MflUser

sub_counties = []
ward_sub_counties = []

sub_counties_file = "/tmp/sub_counties.json"
ward_sub_counties_file = "/tmp/ward_sub_counties.json"
sys_user = MflUser.objects.get(email="system@ehealth.or.ke")


def dump_wards():
    for ward in Ward.objects.all():

        record = {}
        record['code'] = ward.code

        if ward.sub_county:
            record['sub_county'] = ward.sub_county.name

        ward_sub_counties.append(record)

    with open(ward_sub_counties_file, 'w+') as wards_file:
        json.dump(ward_sub_counties, wards_file, indent=4)


def dump_sub_counties():
    for sub_county in SubCounty.objects.all():
        sub_counties.append(
            {
                "name": sub_county.name,
                "county_code": sub_county.county.code
            }
        )

    with open(sub_counties_file, 'w+') as scs_file:
        json.dump(sub_counties, scs_file, indent=4)


def load_wards():
    with open("ward_sub_counties.json") as wards_file:
        data = json.load(wards_file)
        for rec in data:
            if rec.get('sub_county'):
                ward = Ward.objects.get(code=rec.get("code"))
                sub_county = SubCounty.objects.get(
                    name=rec.get('sub_county'))
                ward.sub_county = sub_county
                ward.save()


def load_sub_counties():
    with open("sub_counties.json") as scs_file:
        data = json.load(scs_file)
        for rec in data:
            county = County.objects.get(
                code=rec.get('county_code'))
            try:
                SubCounty.objects.get(name=rec.get("name"))
            except:
                SubCounty.objects.create(
                    name=rec.get('name'),
                    county=county, created_by=sys_user, updated_by=sys_user)

load_sub_counties()
load_wards()
