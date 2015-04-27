from django.conf.urls import url, patterns

from .views import (
    GeoCodeSourceListView,
    GeoCodeSourceDetailView,
    GeoCodeMethodListView,
    GeoCodeMethodDetailView,
    FacilityCoordinatesListView,
    FacilityCoordinatesDetailView,
    WorldBorderListView,
    CountyBoundaryListView,
    ConstituencyBoundaryListView,
    WardBoundaryListView,
    WorldBorderDetailView,
    CountyBoundaryDetailView,
    ConstituencyBoundaryDetailView,
    WardBoundaryDetailView
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

    url(r'^country_borders/$', WorldBorderListView.as_view(),
        name='world_borders_list'),
    url(r'^country_borders/(?P<pk>[^/]+)/$',
        WorldBorderDetailView.as_view(),
        name='world_border_detail'),

    url(r'^county_boundaries/$', CountyBoundaryListView.as_view(),
        name='county_boundaries_list'),
    url(r'^county_boundaries/(?P<pk>[^/]+)/$',
        CountyBoundaryDetailView.as_view(),
        name='county_boundary_detail'),

    url(r'^constituency_boundaries/$', ConstituencyBoundaryListView.as_view(),
        name='constituency_boundaries_list'),
    url(r'^constituency_boundaries/(?P<pk>[^/]+)/$',
        ConstituencyBoundaryDetailView.as_view(),
        name='constituency_boundary_detail'),

    url(r'^ward_boundaries/$', WardBoundaryListView.as_view(),
        name='ward_boundaries_list'),
    url(r'^ward_boundaries/(?P<pk>[^/]+)/$',
        WardBoundaryDetailView.as_view(),
        name='ward_boundary_detail'),
)
