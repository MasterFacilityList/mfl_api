from django.conf.urls import url, patterns

from .views import (
    GeoCodeSourceListView,
    GeoCodeSourceDetailView,
    GeoCodeMethodListView,
    GeoCodeMethodDetailView,
    FacilityCoordinatesListView,
    FacilityCoordinatesDetailView
)


urlpatterns = patterns(
    '',
    url(r'^geo_code_sources/$', GeoCodeSourceListView.as_view(),
        name='geo_code_sources_list'),
    url(r'^geo_code_sources/(?P<pk>[^/]+)/$',
        GeoCodeSourceDetailView.as_view(),
        name='geo_code_source_detail'),

    url(r'^geo_code_methods/$', GeoCodeMethodListView.as_view(),
        name='geo_code_methods_list'),
    url(r'^geo_code_methods/(?P<pk>[^/]+)/$',
        GeoCodeMethodDetailView.as_view(),
        name='geo_code_method_detail'),

    url(r'^coordinates/$', FacilityCoordinatesListView.as_view(),
        name='facility_coordinates_list'),
    url(r'^coordinates/(?P<pk>[^/]+)/$',
        FacilityCoordinatesDetailView.as_view(),
        name='facility_coordinates_detail'),
)
