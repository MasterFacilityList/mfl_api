from django.conf.urls import url, patterns
from django.views.decorators.cache import cache_page
from .views import (
    ContactView,
    ContactDetailView,
    CountyView,
    CountyDetailView,
    ConstituencyView,
    ConstituencyDetailView,
    WardView,
    WardDetailView,
    ContactTypeListView,
    ContactTypeDetailView,
    UserCountyView,
    UserCountyDetailView,
    UserContactListView,
    UserContactDetailView,
    TownListView,
    TownDetailView,
    PhysicalAddressView,
    PhysicalAddressDetailView,
    download_pdf,
    FilteringSummariesView
)


urlpatterns = patterns(
    '',
    url(r'^download_pdf/$',
        download_pdf, name='download_pdf'),

    url(r'^contact_types/$', ContactTypeListView.as_view(),
        name='contact_types_list'),
    url(r'^contact_types/(?P<pk>[^/]+)/$', ContactTypeDetailView.as_view(),
        name='contact_type_detail'),

    url(r'^user_contacts/$', UserContactListView.as_view(),
        name='user_contacts_list'),
    url(r'^user_contacts/(?P<pk>[^/]+)/$', UserContactDetailView.as_view(),
        name='user_contact_detail'),

    url(r'^contacts/$', ContactView.as_view(), name='contacts_list'),
    url(r'^contacts/(?P<pk>[^/]+)/$', ContactDetailView.as_view(),
        name='contact_detail'),

    url(r'^counties/$',
        CountyView.as_view(),
        name='counties_list'),
    url(r'^counties/(?P<pk>[^/]+)/$',
        cache_page(60*60*12)(CountyDetailView.as_view()),
        name='county_detail'),

    url(r'^user_counties/$',
        UserCountyView.as_view(),
        name='user_counties_list'),
    url(r'^user_counties/(?P<pk>[^/]+)/$',
        UserCountyDetailView.as_view(),
        name='user_county_detail'),

    url(r'^wards/$',
        WardView.as_view(),
        name='wards_list'),
    url(r'^wards/(?P<pk>[^/]+)/$',
        cache_page(60*60*12)(WardDetailView.as_view()),
        name='ward_detail'),

    url(r'^towns/$', TownListView.as_view(), name='towns_list'),
    url(r'^towns/(?P<pk>[^/]+)/$', TownDetailView.as_view(),
        name='town_detail'),

    url(r'^constituencies/$',
        ConstituencyView.as_view(),
        name='constituencies_list'),
    url(r'^constituencies/(?P<pk>[^/]+)/$',
        cache_page(60*60*12)(ConstituencyDetailView.as_view()),
        name='constituency_detail'),

    url(r'^address/$', PhysicalAddressView.as_view(),
        name='physical_addresses_list'),
    url(r'^address/(?P<pk>[^/]+)/$',
        PhysicalAddressDetailView.as_view(),
        name='physical_address_detail'),
    url(r'^filtering_summaries/$',
        FilteringSummariesView.as_view(), name="filtering_summaries"),
)
