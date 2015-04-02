from django.conf.urls import url, patterns

from .views import (
    OwnerListView, OwnerDetailView, ServiceListView,
    ServiceDetailView, FacilityListView, FaciltyDetailView)


urlpatterns = patterns(
    '',
    url(r'^owners/$', OwnerListView.as_view(), name='owners_list'),
    url(r'^owners/(?P<id>\w+)/$', OwnerDetailView.as_view(),
        name='owner_detail'),

    url(r'^services/$', ServiceListView.as_view(), name='servicess_list'),
    url(r'^services/(?P<id>\w+)/$', ServiceDetailView.as_view(),
        name='service_detail'),

    url(r'^$', FacilityListView.as_view(), name='facility_list'),
    url(r'^(?P<id>\w+)/$', FaciltyDetailView.as_view(),
        name='facility_detail'),

    url(r'^$', FacilityListView.as_view(), name='facility_list'),
    url(r'^(?P<id>\w+)/$', FaciltyDetailView.as_view(),
        name='facility_detail'),
)
