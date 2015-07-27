from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView, Response
from common.models import County, Constituency, Ward

from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    FacilityType,
    Facility,
)

from ..filters import FacilityFilter


class DashBoard(APIView):
    queryset = Facility.objects.all()
    filter_class = FacilityFilter

    def get_facility_county_summary(self):
        counties = County.objects.all()
        facility_county_summary = {}
        for county in counties:
            facility_county_count = self.queryset.filter(
                ward__constituency__county=county).count()
            facility_county_summary[county.name] = facility_county_count
        top_10_counties = sorted(
            facility_county_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        facility_county_summary
        top_10_counties_summary = []
        for item in top_10_counties:
            top_10_counties_summary.append(
                {
                    "name": item[0],
                    "count": item[1]
                })
        if self.request.user.is_national:
            return top_10_counties_summary
        else:
            return []

    def get_facility_constituency_summary(self):
        constituencies = Constituency.objects.filter(
            county=self.request.user.county)
        constituencies = constituencies if self.request.user.county else []

        facility_constituency_summary = {}
        for const in constituencies:
            facility_const_count = self.queryset.filter(
                ward__constituency=const).count()
            facility_constituency_summary[const.name] = facility_const_count
        top_10_consts = sorted(
            facility_constituency_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        top_10_consts_summary = []
        for item in top_10_consts:
            top_10_consts_summary.append(
                {
                    "name": item[0],
                    "count": item[1]
                })
        return top_10_consts_summary

    def get_facility_ward_summary(self):
        if self.request.user.constituency:
            wards = Ward.objects.filter(
                constituency=self.request.user.constituency)
        else:
            wards = []
        facility_ward_summary = {}
        for ward in wards:
            facility_ward_count = self.queryset.filter(
                ward=ward).count()
            facility_ward_summary[ward.name] = facility_ward_count
        top_10_wards = sorted(
            facility_ward_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        top_10_wards_summary = []
        for item in top_10_wards:
            top_10_wards_summary.append(
                {
                    "name": item[0],
                    "count": item[1]
                })
        return top_10_wards_summary

    def get_facility_type_summary(self):
        facility_types = FacilityType.objects.all()
        facility_type_summary = []
        for facility_type in facility_types:
                facility_type_summary.append(
                    {
                        "name": facility_type.name,
                        "count": self.filter_queryset().filter(
                            facility_type=facility_type).count()
                    })
        facility_type_summary_sorted = sorted(
            facility_type_summary,
            key=lambda x: x, reverse=True)[0:5]

        return facility_type_summary_sorted

    def get_facility_owner_summary(self):
        owners = Owner.objects.all()
        facility_owners_summary = []
        for owner in owners:
            facility_owners_summary.append(
                {
                    "name": owner.name,
                    "count": self.filter_queryset().filter(
                        owner=owner).count()
                })
        return facility_owners_summary

    def get_facility_status_summary(self):
        statuses = FacilityStatus.objects.all()
        status_summary = []
        for status in statuses:
                status_summary.append(
                    {
                        "name": status.name,
                        "count": self.filter_queryset().filter(
                            operation_status=status).count()
                    })

        return status_summary

    def get_facility_owner_types_summary(self):
        owner_types = OwnerType.objects.all()
        owner_types_summary = []
        for owner_type in owner_types:
            owner_types_summary.append(
                {
                    "name": owner_type.name,
                    "count": self.filter_queryset().filter(
                        owner__owner_type=owner_type).count()
                })
        return owner_types_summary

    def get_recently_created_facilities(self):
        right_now = timezone.now()
        three_months_ago = right_now - timedelta(days=90)
        weekly = right_now - timedelta(days=7)
        monthly = right_now - timedelta(days=30)
        weekly = self.request.query_params.get('weekly', None)
        monthly = self.request.query_params.get('monthly', None)
        quarterly = self.request.query_params.get('quarterly', None)
        if quarterly:
            return self.filter_queryset().filter(
                created__gte=three_months_ago).count()
        if monthly:
            return self.filter_queryset().filter(
                created__gte=monthly).count()
        if weekly:
            return self.filter_queryset().filter(
                created__gte=weekly).count()
        return self.filter_queryset().filter(
            created__gte=three_months_ago).count()

    def filter_queryset(self):
        user = self.request.user
        if user.county and not user.is_national:
            return self.queryset.filter(ward__constituency__county=user.county)
        elif user.constituency:
            return self.queryset.filter(ward__constituency=user.constituency)
        elif user.is_national:
            return self.queryset
        else:
            return self.queryset

    def get(self, *args, **kwargs):
        data = {
            "total_facilities": len(self.queryset),
            "county_summary": self.get_facility_county_summary(),
            "constituencies_summary": self.get_facility_constituency_summary(),
            "wards_summary": self.get_facility_ward_summary(),
            "owners_summary": self.get_facility_owner_summary(),
            "types_summary": self.get_facility_type_summary(),
            "status_summary": self.get_facility_status_summary(),
            "owner_types": self.get_facility_owner_types_summary(),
            "recently_created": self.get_recently_created_facilities()
        }

        return Response(data)
