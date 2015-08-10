from facilities.models import Facility
from rest_framework.views import APIView, Response
from common.models import County


class FacilityCountByCountyReport(APIView):
    def get(self, *args, **kwargs):
        counties = County.objects.all()
        facility_county_summary = {}
        for county in counties:
            facility_county_count = Facility.objects.filter(
                ward__constituency__county=county).count()
            facility_county_summary[str(county.name)] = facility_county_count
        top_10_counties = sorted(
            facility_county_summary.items(),
            key=lambda x: x[1], reverse=True)
        facility_county_summary
        counties_summary = []
        for item in top_10_counties:
            counties_summary.append(
                {
                    "county_name": item[0],
                    "number_of_facilities": item[1]
                })
        return Response(data={
            "results": counties_summary,
            "total": Facility.objects.count()
        })
