from django.conf.urls import url, patterns

from ..views import (
    RatingScaleListView, RatingScaleDetailView, RatingListView,
    RatingDetailView, FacilityRatingScaleListView,
    FacilityRatingScaleDetailView, FacilityServiceRatingScaleListView,
    FacilityServiceRatingDetailView, UserFacilityRatingListView,
    UserFacilityRatingDetailView, UserFacilityServiceRatingListView,
    UserFacilityServiceRatingDetailView
)


urlpatterns = patterns(
    '',
    url(r'^scales/$', RatingScaleListView.as_view(),
        name='rating_scales_listy'),
    url(r'^scales/(?P<pk>[^/]+)/$', RatingScaleDetailView.as_view(),
        name='rating_scale_detail'),

    url(r'^ratings/$', RatingListView.as_view(),
        name='rating_list'),
    url(r'^ratings/(?P<pk>[^/]+)/$', RatingDetailView.as_view(),
        name='rating_detail'),

    url(r'^facility_ratings/$', FacilityRatingScaleListView.as_view(),
        name='facility_rating_scale_list'),
    url(r'^facility_ratings/(?P<pk>[^/]+)/$',
        FacilityRatingScaleDetailView.as_view(),
        name='faciity_rating_scale_detail'),

    url(r'^service_scales/$', FacilityServiceRatingScaleListView.as_view(),
        name='service_scale_list'),
    url(r'^service_scales/(?P<pk>[^/]+)/$',
        FacilityServiceRatingDetailView.as_view(),
        name='service_scale_detail'),

    url(r'^user_facility_rating/$', UserFacilityRatingListView.as_view(),
        name='user_facility_rating_list'),
    url(r'^user_facility_rating/(?P<pk>[^/]+)/$',
        UserFacilityRatingDetailView.as_view(),
        name='user_facility_rating_detail'),

    url(r'^user_service_rating/$', UserFacilityServiceRatingListView.as_view(),
        name='user_service_rating_list'),
    url(r'^user_service_rating/(?P<pk>[^/]+)/$',
        UserFacilityServiceRatingDetailView.as_view(),
        name='user_service_rating_detail'),
)
