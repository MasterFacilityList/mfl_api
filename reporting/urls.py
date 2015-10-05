from django.conf.urls import url, patterns

from .facility_reports import (
    ReportView,
    FacilityUpgradeDowngrade,
    CommunityHealthUnitReport
)


urlpatterns = patterns(
    '',
    url(r'^chul/$',
        CommunityHealthUnitReport.as_view(),
        name='chul_reports'),

    url(r'^upgrades_downgrades/$',
        FacilityUpgradeDowngrade.as_view(),
        name='upgrade_downgrade_report'),

    url(r'^$', ReportView.as_view(),
        name='reports'),

)
