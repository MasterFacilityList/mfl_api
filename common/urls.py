from django.conf.urls import url, patterns

from .views import (
    ContactView, ContactDetailView, CountyView, CountyDetailView,
    ConstituencyView, ConstituencyDetailView, WardView,
    WardDetailView, ContactTypeListView, ContactTypeDetailView,
    UserCountiesView, UserCountyDetailView, UserResidenceListView,
    UserResidenceDetailView, api_root)

urlpatterns = patterns(
    '',
    url(r'^api_root/$', api_root, name='url_listing'),

    url(r'^contact_types/$', ContactTypeListView.as_view(),
        name='contact_types_list'),
    url(r'^contact_types/(?P<pk>[^/]+)/$', ContactTypeDetailView.as_view(),
        name='contact_type_detail'),

    url(r'^user_residence/$', UserResidenceListView.as_view(),
        name='user_wards_list'),
    url(r'^user_residence/(?P<pk>[^/]+)/$', UserResidenceDetailView.as_view(),
        name='user_wars_detail'),

    url(r'^contacts/$', ContactView.as_view(), name='contacts_list'),
    url(r'^contacts/(?P<pk>[^/]+)/$', ContactDetailView.as_view(),
        name='contact_detail'),

    url(r'^counties/$', CountyView.as_view(), name='counties_list'),
    url(r'^counties/(?P<pk>[^/]+)/$', CountyDetailView.as_view(),
        name='county_detail'),

    url(r'^counties/$', UserCountiesView.as_view(), name='users_county_list'),
    url(r'^counties/(?P<pk>[^/]+)/$', UserCountyDetailView.as_view(),
        name='user_county_detail'),

    url(r'^wards/$', WardView.as_view(), name='wards_list'),
    url(r'^wards/(?P<pk>[^/]+)/$', WardDetailView.as_view(),
        name='ward_detail'),

    url(r'^constituencies/$', ConstituencyView.as_view(),
        name='constituencies_list'),
    url(r'^constituencies/(?P<pk>[^/]+)/$', ConstituencyDetailView.as_view(),
        name='constituency_detail'),
)
