from django.conf.urls import url, patterns

from .views import (
    ContactView, ContactDetailView, CountyView, CountyDetailView,
    ConstituencyView, ConstituencyDetailView, SubCountyView,
    SubCountyDetailView, ContactTypeListView, ContactTypeDetailView)

urlpatterns = patterns(
    '',
    url(r'^contact_types/$', ContactTypeListView.as_view(),
        name='contact_types_list'),
    url(r'^contact_types/(?P<pk>[^/]+)/$', ContactTypeDetailView.as_view(),
        name='contact_type_detail'),

    url(r'^contacts/$', ContactView.as_view(), name='contacts_list'),
    url(r'^contacts/(?P<pk>[^/]+)/$', ContactDetailView.as_view(),
        name='contact_detail'),

    url(r'^counties/$', CountyView.as_view(), name='counties_list'),
    url(r'^counties/(?P<pk>[^/]+)/$', CountyDetailView.as_view(),
        name='county_detail'),

    url(r'^subcounties/$', SubCountyView.as_view(), name='sub_counties_list'),
    url(r'^subcounties/(?P<pk>[^/]+)/$', SubCountyDetailView.as_view(),
        name='sub_county_detail'),

    url(r'^constituencies/$', ConstituencyView.as_view(),
        name='constituencies_list'),
    url(r'^constituencies/(?P<pk>[^/]+)/$', ConstituencyDetailView.as_view(),
        name='constituency_detail'),
)
