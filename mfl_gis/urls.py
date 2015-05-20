from django.conf import settings
from django.conf.urls import url, patterns
from django.views.decorators.cache import cache_page
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


urlpatterns = patterns(
    '',
    url(r'^geo_code_sources/$',
        cache_page(cache_seconds)(GeoCodeSourceListView.as_view()),
        name='geo_code_sources_list'),
    url(r'^geo_code_sources/(?P<pk>[^/]+)/$',
        cache_page(cache_seconds)(GeoCodeSourceDetailView.as_view()),
        name='geo_code_source_detail'),

    url(r'^geo_code_methods/$',
        cache_page(cache_seconds)(GeoCodeMethodListView.as_view()),
        name='geo_code_methods_list'),
    url(r'^geo_code_methods/(?P<pk>[^/]+)/$',
        cache_page(cache_seconds)(GeoCodeMethodDetailView.as_view()),
        name='geo_code_method_detail'),

    url(r'^coordinates/$',
        cache_page(60)(FacilityCoordinatesListView.as_view()),
        name='facility_coordinates_list'),
    url(r'^coordinates/(?P<pk>[^/]+)/$',
        cache_page(60)(FacilityCoordinatesDetailView.as_view()),
        name='facility_coordinates_detail'),

    url(r'^country_borders/$',
        cache_page(cache_seconds)(WorldBorderListView.as_view()),
        name='world_borders_list'),
    url(r'^country_borders/(?P<pk>[^/]+)/$',
        cache_page(cache_seconds)(WorldBorderDetailView.as_view()),
        name='world_border_detail'),

    url(r'^county_boundaries/$',
        cache_page(cache_seconds)(CountyBoundaryListView.as_view()),
        name='county_boundaries_list'),
    url(r'^county_boundaries/(?P<pk>[^/]+)/$',
        cache_page(cache_seconds)(CountyBoundaryDetailView.as_view()),
        name='county_boundary_detail'),

    url(r'^constituency_boundaries/$',
        cache_page(cache_seconds)(ConstituencyBoundaryListView.as_view()),
        name='constituency_boundaries_list'),
    url(r'^constituency_boundaries/(?P<pk>[^/]+)/$',
        cache_page(cache_seconds)
        (ConstituencyBoundaryDetailView.as_view()),
        name='constituency_boundary_detail'),

    url(r'^ward_boundaries/$',
        cache_page(cache_seconds)(WardBoundaryListView.as_view()),
        name='ward_boundaries_list'),
    url(r'^ward_boundaries/(?P<pk>[^/]+)/$',
        cache_page(cache_seconds)(WardBoundaryDetailView.as_view()),
        name='ward_boundary_detail'),
)
