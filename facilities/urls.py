from django.conf.urls import url, patterns

from .views import (
    FacilityStatusListView, FacilityStatusDetailView, JobTitleListView,
    JobTitleDetailView, OfficerInchargeListView, OfficerInchargeDetailView,
    RegulatingBodyListView, RegulatingBodyDetailView, GeoCodeSourceListView,
    GeoCodeSourceDetailView, ServiceCategoryListView,
    ServiceCategoryDetailView, OwnerTypeListView, OwnerTypeDetailView,
    OfficerInchargeContactListView, OfficerInchargeContactDetailView,
    GeoCodeMethodListView, GeoCodeMethodDetailView, OwnerListView,
    OwnerDetailView, ServiceListView, ServiceDetailView, FacilityListView,
    FaciltyDetailView, FacilityServiceListView, FacilityServiceDetailView,
    FacilityContactListView, FacilityContactDetailView, FacilityGPSListView,
    FacilityGPSDetailView, FacilityRegulationStatusListView,
    FacilityRegulationStatusDetailView, FacilityTypeListView,
    FacilityTypeDetailView, RegulationStatusListView,
    RegulationStatusDetailView)


urlpatterns = patterns(
    '',
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
        name='facility_status_list'),
    url(r'^facility_status/(?P<pk>[^/]+)/$',
        FacilityStatusDetailView.as_view(),
        name='facility_status_detail'),

    url(r'^Officer_contacts/$', OfficerInchargeContactListView.as_view(),
        name='officer_incharge_contact_list'),

    url(r'^Officer_contacts/(?P<pk>[^/]+)/$',
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
        name='facility_regulation_status_list'),
    url(r'^facility_regulation_status/(?P<pk>[^/]+)/$',
        FacilityRegulationStatusDetailView.as_view(),
        name='facility_regulation_status_detail'),

    url(r'^regulation_status/$', RegulationStatusListView.as_view(),
        name='regulation_list'),

    url(r'^regulation_status/(?P<pk>[^/]+)/$',
        RegulationStatusDetailView.as_view(),
        name='regulation_status_detail'),

    url(r'^geo_code_methods/$', GeoCodeMethodListView.as_view(),
        name='geo_code_method_list'),
    url(r'^geo_code_methods/(?P<pk>[^/]+)/$',
        GeoCodeMethodDetailView.as_view(),
        name='geo_code_method_detail'),

    url(r'^officers_incharge/$', OfficerInchargeListView.as_view(),
        name='officers_incharge_list'),
    url(r'^officers_incharge/(?P<pk>[^/]+)/$',
        OfficerInchargeDetailView.as_view(),
        name='officer_incharge_detail'),

    url(r'^service_categories/$', ServiceCategoryListView.as_view(),
        name='service_categories_list'),
    url(r'^service_categories/(?P<pk>[^/]+)/$',
        ServiceCategoryDetailView.as_view(),
        name='sevice_category_detail'),

    url(r'^owner_types/$', OwnerTypeListView.as_view(),
        name='owner_types_list'),
    url(r'^owner_types/(?P<pk>[^/]+)/$', OwnerTypeDetailView.as_view(),
        name='owner_type_detail'),

    url(r'^owners/$', OwnerListView.as_view(), name='owners_list'),
    url(r'^owners/(?P<pk>[^/]+)/$', OwnerDetailView.as_view(),
        name='owner_detail'),

    url(r'^services/$', ServiceListView.as_view(), name='services_list'),
    url(r'^services/(?P<pk>[^/]+)/$', ServiceDetailView.as_view(),
        name='service_detail'),

    url(r'^contacts/$', FacilityContactListView .as_view(),
        name='facilities_contact_list'),

    url(r'^contacts/(?P<pk>[^/]+)/$', FacilityContactDetailView.as_view(),
        name='facility_contact_detail'),

    url(r'^facility_services/$', FacilityServiceListView.as_view(),
        name='facilities_services_list'),

    url(r'^facility_services/(?P<pk>[^/]+)/$',
        FacilityServiceDetailView.as_view(),
        name='facilities_service_detail'),

    url(r'^gis/$', FacilityGPSListView.as_view(), name='facility_gis_list'),
    url(r'^gis/(?P<pk>[^/]+)/$', FacilityGPSDetailView.as_view(),
        name='facilities_gis_detail'),

    url(r'^$', FacilityListView.as_view(), name='facility_list'),
    url(r'^(?P<pk>[^/]+)/$', FaciltyDetailView.as_view(),
        name='facility_detail'),
)
