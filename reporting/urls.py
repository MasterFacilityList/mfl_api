from django.conf.urls import url, patterns

from .facility_reports import ReportView, FacilityUpgradeDowngrade


urlpatterns = patterns(
    '',
    url(r'^upgrades_downgrades/$',
        FacilityUpgradeDowngrade.as_view(),
        name='upgrade_downgrade_report'),
    url(r'^$', ReportView.as_view(),
        name='reports'),

)
