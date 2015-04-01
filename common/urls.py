from django.conf.urls import url, patterns

from .views import (
    ContactView, ContactDetailView, ProvinceView, ProvinceDetailView,
    DisctrictView, DistrictDetailView, DivisionView, DivisionDetailView,
    LocationView, LocationDetailView, SubLocationView, SubLocationDetailView,
    CountyView, CountyDetailView, ConstituencyView, ConstituentcyDetailView)

urlpatterns = patterns(
    '',

    url(r'^contacts/$', ContactView.as_view(), name='contacts_list'),
    url(r'^contact/(?P<id>\w+)/$', ContactDetailView.as_view(),
        name='contact_detail'),

    url(r'^provinces/$', ProvinceView.as_view(), name='provinces_list'),
    url(r'^provinces/(?P<id>\w+)/$', ProvinceDetailView.as_view(),
        name='province_detail'),

    url(r'^counties/$', CountyView.as_view(), name='counties_list'),
    url(r'^counties/(?P<id>\w+)/$', CountyDetailView.as_view(),
        name='county_detail'),

    url(r'^constituencies/$', ConstituencyView.as_view(),
        name='constituencies_list'),
    url(r'^constituencies/(?P<id>\w+)/$', ConstituentcyDetailView.as_view(),
        name='constituency_detail'),

    url(r'^districts/$', DisctrictView.as_view(), name='districts_list'),
    url(r'^districts/(?P<id>\w+)/$', DistrictDetailView.as_view(),
        name='district_detail'),

    url(r'^divisions/$', DivisionView.as_view(), name='division_list'),
    url(r'^divisions/(?P<id>\w+)/$', DivisionDetailView.as_view(),
        name='division_detail'),

    url(r'^locations/$', LocationView.as_view(), name='locations_list'),
    url(r'^locations/(?P<id>\w+)/$', LocationDetailView.as_view(),
        name='location_detail'),

    url(r'^sub_locations/$', SubLocationView.as_view(),
        name='sub_locations_list'),
    url(r'^sub_locations/(?P<id>\w+)/$', SubLocationDetailView.as_view(),
        name='sub_location_detail'),
)
