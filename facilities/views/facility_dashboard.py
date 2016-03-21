from datetime import timedelta

from django.utils import timezone
from django.db.models import Q

from rest_framework.views import APIView, Response
from common.models import County, SubCounty, Ward
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

    def get_chu_count_in_county_summary(self, county):
        return CommunityHealthUnit.objects.filter(
            facility__ward__sub_county__county=county).count()

    def get_chu_count_in_constituency_summary(self, const):
        return CommunityHealthUnit.objects.filter(
            facility__ward__sub_county=const).count()

    def get_chu_count_in_ward_summary(self, ward):
        return CommunityHealthUnit.objects.filter(
            facility__ward=ward).count()

    def get_facility_county_summary(self):
        counties = County.objects.all()
        facility_county_summary = {}
        for county in counties:
            facility_county_count = self.get_queryset().filter(
                ward__sub_county__county=county).count()
            facility_county_summary[str(county.name)] = facility_county_count

        top_10_counties = sorted(
            facility_county_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        facility_county_summary
        top_10_counties_summary = []
        for item in top_10_counties:
            county = County.objects.get(name=item[0])
            chu_count = self.get_chu_count_in_county_summary(county)
            top_10_counties_summary.append(
                {
                    "name": item[0],
                    "count": item[1],
                    "chu_count": chu_count
                })
        return top_10_counties_summary if self.request.user.is_national else []

    def get_facility_constituency_summary(self):
        constituencies = SubCounty.objects.filter(
            county=self.request.user.county)
        constituencies = constituencies if self.request.user.county else []

        facility_constituency_summary = {}
        for const in constituencies:
            facility_const_count = self.get_queryset().filter(
                ward__sub_county=const).count()
            facility_constituency_summary[
                str(const.name)] = facility_const_count
        top_10_consts = sorted(
            facility_constituency_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        top_10_consts_summary = []
        for item in top_10_consts:
            const = SubCounty.objects.get(name=item[0])
            chu_count = self.get_chu_count_in_constituency_summary(const)
            top_10_consts_summary.append(
                {
                    "name": item[0],
                    "count": item[1],
                    "chu_count": chu_count
                })
        return top_10_consts_summary

    def get_facility_ward_summary(self):
        wards = Ward.objects.filter(
            sub_county=self.request.user.sub_county) \
            if self.request.user.sub_county else []
        facility_ward_summary = {}
        for ward in wards:
            facility_ward_count = self.get_queryset().filter(
                ward=ward).count()
            facility_ward_summary[
                str(ward.name + "|" + str(ward.code))] = facility_ward_count
        top_10_wards = sorted(
            facility_ward_summary.items(),
            key=lambda x: x[1], reverse=True)[0:20]
        top_10_wards_summary = []
        for item in top_10_wards:
            ward = Ward.objects.get(code=item[0].split('|')[1])
            chu_count = self.get_chu_count_in_ward_summary(ward)
            top_10_wards_summary.append(
                {
                    "name": item[0].split('|')[0],
                    "count": item[1],
                    "chu_count": chu_count
                })
        return top_10_wards_summary

    def get_facility_type_summary(self):
        facility_types = FacilityType.objects.all()
        facility_type_summary = []
        for facility_type in facility_types:
                facility_type_summary.append(
                    {
                        "name": str(facility_type.name),
                        "count": self.get_queryset().filter(
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
                    "count": self.get_queryset().filter(
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
                        "count": self.get_queryset().filter(
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
                    "count": self.get_queryset().filter(
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
            return self.get_queryset().filter(
                created__gte=weekly).count()

        if last_month:
            monthly = right_now - timedelta(days=30)
            return self.get_queryset().filter(
                created__gte=monthly).count()

        if last_three_months:
            return self.get_queryset().filter(
                created__gte=three_months_ago).count()

        return self.get_queryset().filter(
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

    def facilities_pending_approval_count(self):
        updated_pending_approval = self.get_queryset().filter(has_edits=True)
        newly_created = self.queryset.filter(approved=False, rejected=False)
        return len(
            list(set(list(updated_pending_approval) + list(newly_created)))
        )

    def get_chus_pending_approval(self):
        """
        Get the number of CHUs pending approval
        """

        return CommunityHealthUnit.objects.filter(
            Q(is_approved=False, is_rejected=False) |
            Q(has_edits=True)).distinct().filter(
                facility__in=self.get_queryset()).count()

    def get_rejected_chus(self):
        """
        Get the number of CHUs that have been rejected
        """
        return CommunityHealthUnit.objects.filter(is_rejected=True).count()

    def get_rejected_facilities_count(self):
        return self.get_queryset().filter(rejected=True).count()

    def get_closed_facilities_count(self):
        return self.get_queryset().filter(closed=True).count()

    def get(self, *args, **kwargs):
        user = self.request.user
        data = {
            "total_facilities": self.get_queryset().count(),
            "county_summary": self.get_facility_county_summary()
            if user.is_national else [],
            "constituencies_summary": self.get_facility_constituency_summary()
            if user.county else [],
            "wards_summary": self.get_facility_ward_summary()
            if user.constituency else [],
            "owners_summary": self.get_facility_owner_summary(),
            "types_summary": self.get_facility_type_summary(),
            "status_summary": self.get_facility_status_summary(),
            "owner_types": self.get_facility_owner_types_summary(),
            "recently_created": self.get_recently_created_facilities(),
            "recently_created_chus": self.get_recently_created_chus(),
            "pending_updates": self.facilities_pending_approval_count(),
            "rejected_facilities_count": self.get_rejected_facilities_count(),
            "closed_facilities_count": self.get_closed_facilities_count(),
            "rejected_chus": self.get_rejected_chus(),
            "chus_pending_approval": self.get_chus_pending_approval(),
            "total_chus": CommunityHealthUnit.objects.filter(
                facility__in=self.get_queryset()).count()

        }
        fields = self.request.query_params.get("fields", None)
        if fields:
            required = fields.split(",")
            required_data = {
                i: data[i] for i in data if i in required
            }
            return Response(required_data)
        return Response(data)
