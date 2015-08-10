from django.conf.urls import url, patterns

from .facility_reports import FacilityCountByCountyReport


urlpatterns = patterns(
    '',
    url(r'^facilitiies_by_county/$', FacilityCountByCountyReport.as_view(),
        name='facility_by_county_report'),
)
