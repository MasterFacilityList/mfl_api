from django.conf import settings
from django.conf.urls import url, patterns
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
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


cache_seconds = settings.GIS_BORDERS_CACHE_SECONDS
coordinates_cache_seconds = (60 * 60 * 24)


urlpatterns = patterns(
    '',
    url(r'^geo_code_sources/$',
        gzip_page(
            cache_page(cache_seconds)
            (GeoCodeSourceListView.as_view())),
        name='geo_code_sources_list'),
    url(r'^geo_code_sources/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (GeoCodeSourceDetailView.as_view())),
        name='geo_code_source_detail'),

    url(r'^geo_code_methods/$',
        gzip_page(
            cache_page(cache_seconds)
            (GeoCodeMethodListView.as_view())),
        name='geo_code_methods_list'),
    url(r'^geo_code_methods/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (GeoCodeMethodDetailView.as_view())),
        name='geo_code_method_detail'),

    url(r'^coordinates/$',
        gzip_page(
            cache_page(coordinates_cache_seconds)
            (FacilityCoordinatesListView.as_view())),
        name='facility_coordinates_list'),
    url(r'^coordinates/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(coordinates_cache_seconds)
            (FacilityCoordinatesDetailView.as_view())),
        name='facility_coordinates_detail'),

    url(r'^country_borders/$',
        gzip_page(
            cache_page(cache_seconds)
            (WorldBorderListView.as_view())),
        name='world_borders_list'),
    url(r'^country_borders/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (WorldBorderDetailView.as_view())),
        name='world_border_detail'),

    url(r'^county_boundaries/$',
        gzip_page(
            cache_page(cache_seconds)
            (CountyBoundaryListView.as_view())),
        name='county_boundaries_list'),
    url(r'^county_boundaries/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (CountyBoundaryDetailView.as_view())),
        name='county_boundary_detail'),

    url(r'^constituency_boundaries/$',
        gzip_page(
            cache_page(cache_seconds)
            (ConstituencyBoundaryListView.as_view())),
        name='constituency_boundaries_list'),
    url(r'^constituency_boundaries/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (ConstituencyBoundaryDetailView.as_view())),
        name='constituency_boundary_detail'),

    url(r'^ward_boundaries/$',
        gzip_page(
            cache_page(cache_seconds)
            (WardBoundaryListView.as_view())),
        name='ward_boundaries_list'),
    url(r'^ward_boundaries/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (WardBoundaryDetailView.as_view())),
        name='ward_boundary_detail'),
)
