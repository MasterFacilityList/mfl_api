from django.conf.urls import url, patterns

from .views import (
    ContactView, ContactDetailView, CountyView, CountyDetailView,
    ConstituencyView, ConstituencyDetailView, SubCountyView,
    SubCountyDetailView, ContactTypeListView, ContactTypeDetailView)

urlpatterns = patterns(
    '',
    url(r'^contact_types/$', ContactTypeListView.as_view(),
        name='contacts_types_list'),
    url(r'^contact_types/(?P<pk>\w+)/$', ContactTypeDetailView.as_view(),
        name='contact_type_detail'),

    url(r'^contacts/$', ContactView.as_view(), name='contacts_list'),
    url(r'^contact/(?P<pk>\w+)/$', ContactDetailView.as_view(),
        name='contact_detail'),

    url(r'^counties/$', CountyView.as_view(), name='counties_list'),
    url(r'^counties/(?P<pk>\w+)/$', CountyDetailView.as_view(),
        name='county_detail'),

    url(r'^subcounties/$', SubCountyView.as_view(), name='sub_counties_list'),
    url(r'^subcounties/(?P<pk>\w+)/$', SubCountyDetailView.as_view(),
        name='sub_county_detail'),

    url(r'^constituencies/$', ConstituencyView.as_view(),
        name='constituencies_list'),
    url(r'^constituencies/(?P<pk>\w+)/$', ConstituencyDetailView.as_view(),
        name='constituency_detail'),
)
