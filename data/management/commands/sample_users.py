from django.contrib.auth.models import make_password, Group

from django.core.management import BaseCommand
from users.models import MflUser
from common.models import County, Constituency, UserCounty, UserConstituency

system_user = MflUser.objects.get(email='system@ehealth.or.ke')


class Command(BaseCommand):

    def handle(self, *args, **options):
        chrio = Group.objects.get(
            name="County Health Records Information Officer")
        schrio = Group.objects.get(
            name="Sub County Health Records Information Officer")

        for county in County.objects.all():
            user_data = {
                "email": "{}@mfltest.slade360.co.ke".format(
                    county.name.lower()),
                "first_name": "{}".format(county.name.lower()),
                "last_name": "{}".format(county.name.lower()),
                "username": "{}".format(county.name.lower()),
                "password": make_password(county.name.lower()),
                "employee_number": county.code * 825,
            }
            try:
                user_obj = MflUser.objects.get(email=user_data['email'])
            except MflUser.DoesNotExist:
                user_obj = MflUser.objects.create(**user_data)

            try:
                UserCounty.objects.get(user=user_obj)
            except UserCounty.DoesNotExist:
                UserCounty.objects.create(
                    user=user_obj, county=county, created_by=user_obj,
                    updated_by=user_obj)
            user_obj.groups.add(chrio)

        for const in Constituency.objects.all():
            user_data = {
                "email": "{}@mfltest.slade360.co.ke".format(
                    const.name.lower()),
                "first_name": "{}".format(const.name.lower()),
                "last_name": "{}".format(const.name.lower()),
                "username": "{}".format(const.name.lower()),
                "password": make_password(const.name.lower()),
                "employee_number": const.code * 2535,
            }
            try:
                user_obj = MflUser.objects.get(email=user_data['email'])
            except MflUser.DoesNotExist:
                user_obj = MflUser.objects.create(**user_data)

            county_chrio = UserCounty.objects.filter(
                county=const.county)[0].user
            try:
                UserConstituency.objects.get(user=user_obj)
            except UserConstituency.DoesNotExist:
                UserConstituency.objects.create(
                    constituency=const, user=user_obj,
                    created_by=county_chrio, updated_by=county_chrio)
            user_obj.groups.add(schrio)
