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
    WardBoundaryDetailView,
    FacilityCoordinatesCreationAndListing,
    FacilityCoordinatesCreationAndDetail,
    ConstituencyBoundView,
    CountyBoundView,
    IkoWapi,
    DrillFacilityCoords,
    DrillCountryBorders,
    DrillCountyBorders,
    DrillConstituencyBorders,
    DrillWardBorders,
)


cache_seconds = settings.GIS_BORDERS_CACHE_SECONDS
coordinates_cache_seconds = (60 * 60 * 24)


urlpatterns = patterns(
    '',

    url(
        r'^drilldown/facility/$',
        cache_page(60*60)(DrillFacilityCoords.as_view()),
        name='drilldown_facility'
    ),
    url(
        r'^drilldown/country/$',
        cache_page(coordinates_cache_seconds)(DrillCountryBorders.as_view()),
        name='drilldown_country'
    ),
    url(
        r'^drilldown/county/(?P<code>\d{1,5})/$',
        cache_page(coordinates_cache_seconds)(DrillCountyBorders.as_view()),
        name='drilldown_county'
    ),
    url(
        r'^drilldown/constituency/(?P<code>\d{1,5})/$',
        cache_page(coordinates_cache_seconds)(
            DrillConstituencyBorders.as_view()
        ),
        name='drilldown_constituency'
    ),
    url(
        r'^drilldown/ward/(?P<code>\d{1,5})/$',
        cache_page(coordinates_cache_seconds)(DrillWardBorders.as_view()),
        name='drilldown_ward'
    ),

    url(r'^ikowapi/$', IkoWapi.as_view(), name='ikowapi'),

    url(r'^geo_code_sources/$',
        GeoCodeSourceListView.as_view(),
        name='geo_code_sources_list'),
    url(r'^geo_code_sources/(?P<pk>[^/]+)/$',
        GeoCodeSourceDetailView.as_view(),
        name='geo_code_source_detail'),

    url(r'^geo_code_methods/$',
        GeoCodeMethodListView.as_view(),
        name='geo_code_methods_list'),
    url(r'^geo_code_methods/(?P<pk>[^/]+)/$',
        GeoCodeMethodDetailView.as_view(),
        name='geo_code_method_detail'),

    url(r'^facility_coordinates/(?P<pk>[^/]+)/$',
        FacilityCoordinatesCreationAndDetail.as_view(),
        name='facility_coordinates_simple_detail'),

    url(r'^facility_coordinates/$',
        FacilityCoordinatesCreationAndListing.as_view(),
        name='facility_coordinates_simple_list'),
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
    url(r'^county_bound/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (CountyBoundView.as_view())),
        name='county_bound'),

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

    url(r'^constituency_bound/(?P<pk>[^/]+)/$',
        gzip_page(
            cache_page(cache_seconds)
            (ConstituencyBoundView.as_view())),
        name='constituency_bound'),

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
