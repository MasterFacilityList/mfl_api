from django.conf.urls import url, patterns

from .facility_reports import ReportView


urlpatterns = patterns(
    '',
    url(r'^$', ReportView.as_view(),
        name='reports'),

)
