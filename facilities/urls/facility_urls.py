from django.conf.urls import url, patterns

from ..views import (
    FacilityStatusListView, FacilityStatusDetailView, JobTitleListView,
    JobTitleDetailView, OfficerInchargeListView, OfficerInchargeDetailView,
    RegulatingBodyListView, RegulatingBodyDetailView, GeoCodeSourceListView,
    GeoCodeSourceDetailView, OwnerTypeListView, OwnerTypeDetailView,
    OfficerInchargeContactListView, OfficerInchargeContactDetailView,
    GeoCodeMethodListView, GeoCodeMethodDetailView, OwnerListView,
    OwnerDetailView, FacilityListView,
    FacilityDetailView,
    FacilityContactListView, FacilityContactDetailView,
    FacilityCoordinatesListView,
    FacilityCoordinatesDetailView, FacilityRegulationStatusListView,
    FacilityRegulationStatusDetailView, FacilityTypeListView,
    FacilityTypeDetailView, RegulationStatusListView,
    RegulationStatusDetailView, FacilityUnitsListView, FacilityUnitDetailView
)


urlpatterns = patterns(
    '',

    url(r'^facility_units/$', FacilityUnitsListView.as_view(),
        name='facility_units_list'),
    url(r'^facility_units/(?P<pk>[^/]+)/$', FacilityUnitDetailView.as_view(),
        name='facility_unit_detail'),

    url(r'^regulating_bodies/$', RegulatingBodyListView.as_view(),
        name='regulating_bodies_list'),
    url(r'^regulating_bodies/(?P<pk>[^/]+)/$',
        RegulatingBodyDetailView.as_view(),
        name='regulating_body_detail'),

    url(r'^facility_types/$', FacilityTypeListView.as_view(),
        name='facility_types_list'),
    url(r'^facility_types/(?P<pk>[^/]+)/$', FacilityTypeDetailView.as_view(),
        name='facility_type_detail'),

    url(r'^facility_status/$', FacilityStatusListView.as_view(),
        name='facility_statuses_list'),
    url(r'^facility_status/(?P<pk>[^/]+)/$',
        FacilityStatusDetailView.as_view(),
        name='facility_status_detail'),

    url(r'^officer_contacts/$', OfficerInchargeContactListView.as_view(),
        name='officer_incharge_contacts_list'),
    url(r'^officer_contacts/(?P<pk>[^/]+)/$',
        OfficerInchargeContactDetailView.as_view(),
        name='officer_incharge_contact_detail'),

    url(r'^job_titles/$', JobTitleListView.as_view(),
        name='job_titles_list'),
    url(r'^job_titles/(?P<pk>[^/]+)/$', JobTitleDetailView.as_view(),
        name='job_title_detail'),

    url(r'^geo_code_sources/$', GeoCodeSourceListView.as_view(),
        name='geo_code_sources_list'),
    url(r'^geo_code_sources/(?P<pk>[^/]+)/$',
        GeoCodeSourceDetailView.as_view(),
        name='geo_code_source_detail'),

    url(r'^facility_regulation_status/$',
        FacilityRegulationStatusListView.as_view(),
        name='facility_regulation_statuses_list'),
    url(r'^facility_regulation_status/(?P<pk>[^/]+)/$',
        FacilityRegulationStatusDetailView.as_view(),
        name='facility_regulation_status_detail'),

    url(r'^regulation_status/$', RegulationStatusListView.as_view(),
        name='regulation_statuses_list'),
    url(r'^regulation_status/(?P<pk>[^/]+)/$',
        RegulationStatusDetailView.as_view(),
        name='regulation_status_detail'),

    url(r'^geo_code_methods/$', GeoCodeMethodListView.as_view(),
        name='geo_code_methods_list'),
    url(r'^geo_code_methods/(?P<pk>[^/]+)/$',
        GeoCodeMethodDetailView.as_view(),
        name='geo_code_method_detail'),

    url(r'^officers_incharge/$', OfficerInchargeListView.as_view(),
        name='officers_in_charge_list'),
    url(r'^officers_incharge/(?P<pk>[^/]+)/$',
        OfficerInchargeDetailView.as_view(),
        name='officer_incharge_detail'),

    url(r'^owner_types/$', OwnerTypeListView.as_view(),
        name='owner_types_list'),
    url(r'^owner_types/(?P<pk>[^/]+)/$', OwnerTypeDetailView.as_view(),
        name='owner_type_detail'),

    url(r'^owners/$', OwnerListView.as_view(), name='owners_list'),
    url(r'^owners/(?P<pk>[^/]+)/$', OwnerDetailView.as_view(),
        name='owner_detail'),

    url(r'^contacts/$', FacilityContactListView .as_view(),
        name='facility_contacts_list'),
    url(r'^contacts/(?P<pk>[^/]+)/$', FacilityContactDetailView.as_view(),
        name='facility_contact_detail'),

    url(r'^coordinates/$', FacilityCoordinatesListView.as_view(),
        name='facility_coordinates_list'),
    url(r'^coordinates/(?P<pk>[^/]+)/$',
        FacilityCoordinatesDetailView.as_view(),
        name='facility_coordinates_detail'),

    url(r'^facilities/$', FacilityListView.as_view(), name='facilities_list'),
    url(r'^facilities/(?P<pk>[^/]+)/$', FacilityDetailView.as_view(),
        name='facility_detail'),
)
