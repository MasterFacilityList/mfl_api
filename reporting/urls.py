from django.conf.urls import url, patterns

from .facility_reports import (
    FacilityCountByCountyReport,
    FacilityCountyByConstituencyReport,
    FaclityCountyByOwnerCategory)


urlpatterns = patterns(
    '',
    url(r'^facility_count_by_county/$', FacilityCountByCountyReport.as_view(),
        name='facility_count_by_county'),
    url(r'^facility_count_by_constituency/$',
        FacilityCountyByConstituencyReport.as_view(),
        name='facility_count_by_constituency'),
    url(r'^facility_count_by_owner_category/$',
        FaclityCountyByOwnerCategory.as_view(),
        name='facility_count_by_owner_category'),
)
