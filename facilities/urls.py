from django.conf.urls import url, patterns

from .views import (
    OwnerListView, OwnerDetailView, ServiceListView,
    ServiceDetailView, FacilityListView, FaciltyDetailView,
    FacilityContactListView, FacilityContactDetailView,
    FacilityServiceListView, FacilityServiceDetailView, FacilityGPSListView,
    FacilityGPSDetailView)


urlpatterns = patterns(
    '',
    url(r'^owners/$', OwnerListView.as_view(), name='owners_list'),
    url(r'^owners/(?P<pk>[^/]+)/$', OwnerDetailView.as_view(),
        name='owner_detail'),

    url(r'^services/$', ServiceListView.as_view(), name='servicess_list'),
    url(r'^services/(?P<pk>[^/]+)/$', ServiceDetailView.as_view(),
        name='service_detail'),

    url(r'^contacts/$', FacilityContactListView .as_view(),
        name='facilities_contact_list'),

    url(r'^contacts/(?P<pk>[^/]+)/$', FacilityContactDetailView.as_view(),
        name='facility_contact_detail'),

    url(r'^facility_services/$', FacilityServiceListView.as_view(),
        name='facilities_services_list'),

    url(r'^facility_services/(?P<pk>[^/]+)/$',
        FacilityServiceDetailView.as_view(),
        name='facilities_service_detail'),

    url(r'^gis/$', FacilityGPSListView.as_view(), name='facility_gis_list'),
    url(r'^gis/(?P<pk>[^/]+)/$', FacilityGPSDetailView.as_view(),
        name='facilities_gis_detail'),

    url(r'^$', FacilityListView.as_view(), name='facility_list'),
    url(r'^(?P<pk>[^/]+)/$', FaciltyDetailView.as_view(),
        name='facility_detail'),
)
