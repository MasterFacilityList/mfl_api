from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView, Response
from common.models import County, Constituency, Ward
from chul.models import CommunityHealthUnit

from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    FacilityType,
    Facility
)
from ..views import QuerysetFilterMixin


class DashBoard(QuerysetFilterMixin, APIView):
    queryset = Facility.objects.all()

    def get_facility_county_summary(self):
        counties = County.objects.all()
        facility_county_summary = {}
        for county in counties:
            facility_county_count = self.filter_queryset().filter(
                ward__constituency__county=county).count()
            facility_county_summary[str(county.name)] = facility_county_count
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
            facility_const_count = self.filter_queryset().filter(
                ward__constituency=const).count()
            facility_constituency_summary[
                str(const.name)] = facility_const_count
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
            facility_ward_count = self.filter_queryset().filter(
                ward=ward).count()
            facility_ward_summary[str(ward.name)] = facility_ward_count
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
        last_week = self.request.query_params.get('last_week', None)
        last_month = self.request.query_params.get('last_month', None)
        last_three_months = self.request.query_params.get(
            'last_three_months', None)
        three_months_ago = right_now - timedelta(days=90)
        if last_week:
            weekly = right_now - timedelta(days=7)
            return self.filter_queryset().filter(
                created__gte=weekly).count()

        if last_month:
            monthly = right_now - timedelta(days=30)
            return self.filter_queryset().filter(
                created__gte=monthly).count()

        if last_three_months:
            return self.filter_queryset().filter(
                created__gte=three_months_ago).count()

        return self.filter_queryset().filter(
            created__gte=three_months_ago).count()

    def get_recently_created_chus(self):
        right_now = timezone.now()
        last_week = self.request.query_params.get('last_week', None)
        last_month = self.request.query_params.get('last_month', None)
        last_three_months = self.request.query_params.get(
            'last_three_months', None)
        three_months_ago = right_now - timedelta(days=90)
        if last_week:
            weekly = right_now - timedelta(days=7)
            return CommunityHealthUnit.objects.filter(
                facility__in=self.get_queryset(),
                created__gte=weekly).count()

        if last_month:
            monthly = right_now - timedelta(days=30)
            return CommunityHealthUnit.objects.filter(
                facility__in=self.get_queryset(),
                created__gte=monthly).count()

        if last_three_months:
            return CommunityHealthUnit.objects.filter(
                facility__in=self.get_queryset(),
                date_established__gte=three_months_ago).count()

        return CommunityHealthUnit.objects.filter(
            facility__in=self.get_queryset(),
            date_established__gte=three_months_ago).count()

    def get_facility_with_pending_updates(self):
        return self.filter_queryset().filter(has_edits=True).count()

    def filter_queryset(self):
        return self.get_queryset()
        # user = self.request.user
        # if user.county and not user.is_national:
        #     return self.get_queryset().filter(
        #         ward__constituency__county=user.county)
        # elif user.constituency:
        #     return self.get_queryset().filter(
        #         ward__constituency__county=user.constituency.county)
        # elif user.is_national:
        #     return self.get_queryset()
        # else:
        #     return self.get_queryset

    def facilities_pending_approval_count(self):
        updated_pending_approval = self.get_queryset().filter(has_edits=True)
        newly_created = self.queryset.filter(approved=False, rejected=False)
        return len(list(set(list(updated_pending_approval) + list(newly_created))))

    def get(self, *args, **kwargs):
        data = {
            "total_facilities": len(self.filter_queryset()),
            "county_summary": self.get_facility_county_summary(),
            "constituencies_summary": self.get_facility_constituency_summary(),
            "wards_summary": self.get_facility_ward_summary(),
            "owners_summary": self.get_facility_owner_summary(),
            "types_summary": self.get_facility_type_summary(),
            "status_summary": self.get_facility_status_summary(),
            "owner_types": self.get_facility_owner_types_summary(),
            "recently_created": self.get_recently_created_facilities(),
            "recently_created_chus": self.get_recently_created_chus(),
            "facilities_pending_approval_count": self.facilities_pending_approval_count(),
            "pending_updates": self.get_facility_with_pending_updates()
        }
        fields = self.request.query_params.get("fields", None)
        if fields:
            required = fields.split(",")
            required_data = {
                i: data[i] for i in data if i in required
            }
            return Response(required_data)
        return Response(data)
