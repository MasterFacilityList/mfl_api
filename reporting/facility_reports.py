from facilities.models import Facility, OwnerType
from rest_framework.views import APIView, Response
from common.models import County, Constituency


class FacilityCountByCountyReport(APIView):
    def get(self, *args, **kwargs):
        counties = County.objects.all()
        facility_county_summary = {}
        for county in counties:
            facility_county_count = Facility.objects.filter(
                ward__constituency__county=county).count()
            facility_county_summary[str(county.name)] = facility_county_count
        top_counties = sorted(
            facility_county_summary.items(),
            key=lambda x: x[1], reverse=True)
        facility_county_summary
        counties_summary = []
        for item in top_counties:
            counties_summary.append(
                {
                    "county_name": item[0],
                    "number_of_facilities": item[1]
                })
        return Response(data={
            "results": counties_summary,
            "total": Facility.objects.count()
        })


class FacilityCountyByConstituencyReport(APIView):
    def get(self, *args, **kwargs):
        constituencies = Constituency.objects.all()

        facility_constituency_summary = {}
        for const in constituencies:
            facility_const_count = Facility.objects.filter(
                ward__constituency=const).count()
            facility_constituency_summary[
                str(const.name)] = facility_const_count
        consts = sorted(
            facility_constituency_summary.items(),
            key=lambda x: x[1], reverse=True)
        consts_summary = []
        for item in consts:
            consts_summary.append(
                {
                    "constituency_name": item[0],
                    "number_of_facilities": item[1]
                })
        return Response(
            data={
                "results": consts_summary,
                "total": Facility.objects.count()
            }
        )


class FaclityCountyByOwnerCategory(APIView):
    def get(self, *args, **kwargs):
        owner_types = OwnerType.objects.all()
        owner_types_summary = []
        for owner_type in owner_types:
            owner_types_summary.append(
                {
                    "type_category": owner_type.name,
                    "number_of_facilities": Facility.objects.filter(
                        owner__owner_type=owner_type).count()
                })
        data = {
            "results": owner_types_summary,
            "total": Facility.objects.count()
        }
        return Response(data=data)
