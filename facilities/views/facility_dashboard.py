from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView, Response
from common.models import County, Constituency

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

    def get_facility_type_summary(self):
        facility_types = FacilityType.objects.all()
        facility_type_summary = []
        for facility_type in facility_types:
            if self.request.user.is_national:
                facility_type_count = self.queryset.filter(
                    facility_type=facility_type).count()
                facility_type_summary.append(
                    {
                        "name": facility_type.name,
                        "count": facility_type_count
                    })
            else:
                facility_type_count = self.queryset.filter(
                    facility_type=facility_type,
                    ward__constituency__county=self.request.user.county
                ).count()
                facility_type_summary.append(
                    {
                        "name": facility_type.name,
                        "count": facility_type_count
                    })
        facility_type_summary_sorted = sorted(
            facility_type_summary,
            key=lambda x: x, reverse=True)[0:5]

        return facility_type_summary_sorted

    def get_facility_owner_summary(self):
        owners = Owner.objects.all()
        facility_owners_summary = []
        for owner in owners:
            owner_count = self.queryset.filter(owner=owner).count()
            facility_owners_summary.append(
                {
                    "name": owner.name,
                    "count": owner_count
                })
        return facility_owners_summary

    def get_facility_status_summary(self):
        statuses = FacilityStatus.objects.all()
        status_summary = []
        for status in statuses:
            if not self.request.user.is_national:
                status_count = Facility.objects.filter(
                    operation_status=status,
                    ward__constituency__county=self.request.user.county
                ).count()
                status_summary.append(
                    {
                        "name": status.name,
                        "count": status_count

                    })
            else:
                status_count = Facility.objects.filter(
                    operation_status=status).count()
                status_summary.append(
                    {
                        "name": status.name,
                        "count": status_count
                    })
        return status_summary

    def get_facility_owner_types_summary(self):
        owner_types = OwnerType.objects.all()
        owner_types_summary = []
        for owner_type in owner_types:
            if self.request.user.is_national:
                owner_types_count = Facility.objects.filter(
                    owner__owner_type=owner_type).count()
                owner_types_summary.append(
                    {
                        "name": owner_type.name,
                        "count": owner_types_count
                    })
            else:
                owner_types_count = Facility.objects.filter(
                    owner__owner_type=owner_type,
                    ward__constituency__county=self.request.user.county
                ).count()
                owner_types_summary.append(
                    {
                        "name": owner_type.name,
                        "count": owner_types_count
                    })
        return owner_types_summary

    def get_recently_created_facilities(self):
        right_now = timezone.now()
        three_months_ago = right_now - timedelta(days=90)
        recent_facilities_count = 0
        if self.request.user.is_national:
            recent_facilities_count = Facility.objects.filter(
                created__gte=three_months_ago).count()
        else:
            recent_facilities_count = Facility.objects.filter(
                created__gte=three_months_ago,
                ward__constituency__county=self.request.user.county).count()
        return recent_facilities_count

    def get_owner_count(self):
        if self.request.user.is_national:
            return Owner.objects.count()
        else:
            return len(list(set(
                [
                    f.owner for f in Facility.objects.filter(
                        ward__constituency__county=self.request.user.county)
                ]
            )))

    def get(self, *args, **kwargs):
        total_facilities = 0
        if self.request.user.is_national:
            total_facilities = Facility.objects.count()
        else:
            total_facilities = Facility.objects.filter(
                ward__constituency__county=self.request.user.county
            ).count()

        data = {
            "total_facilities": total_facilities,
            "county_summary": self.get_facility_county_summary(),
            "constituencies_summary": self.get_facility_constituency_summary(),
            "owners_summary": self.get_facility_owner_summary(),
            "types_summary": self.get_facility_type_summary(),
            "status_summary": self.get_facility_status_summary(),
            "owner_types": self.get_facility_owner_types_summary(),
            "recently_created": self.get_recently_created_facilities(),
            "owner_count": self.get_owner_count()
        }

        return Response(data)
