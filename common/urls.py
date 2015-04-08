from django.conf.urls import url, patterns

from .views import (
    ContactView, ContactDetailView, CountyView, CountyDetailView,
    ConstituencyView, ConstituentcyDetailView, SubCountyView,
    SubCountyDetailView)

urlpatterns = patterns(
    '',

    url(r'^contacts/$', ContactView.as_view(), name='contacts_list'),
    url(r'^contact/(?P<id>\w+)/$', ContactDetailView.as_view(),
        name='contact_detail'),


    url(r'^counties/$', CountyView.as_view(), name='counties_list'),
    # url(r'^counties/(?P<id>\w+)/$', CountyDetailView.as_view(),
    #     name='county_detail'),

    url(r'^subcounties/$', SubCountyView.as_view(), name='sub_counties_list'),
    url(r'^subcounties/(?P<id>\w+)/$', SubCountyDetailView.as_view(),
        name='sub_county_detail'),

    url(r'^constituencies/$', ConstituencyView.as_view(),
        name='constituencies_list'),
    url(r'^constituencies/(?P<id>\w+)/$', ConstituentcyDetailView.as_view(),
        name='constituency_detail'),
)
