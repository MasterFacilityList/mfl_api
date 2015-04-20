from django.conf.urls import url, patterns

from ..views import (
    PracticeTypeListView,
    PracticeTypeDetailView,
    SpecialityListView,
    SpecialityDetailView,
    QualificationListView,
    QualificationDetailView,
    PractitionerListView,
    PractitionerDetailView,
    PractitionerQualificationListView,
    PractitionerQualificationDetailView,
    PractitionerContactListView,
    PractitionerContactDetailView,
    PractitionerFacilityListView,
    PractitionerFacilityDetailView
)


urlpatterns = patterns(
    '',
    url(r'^practice_types/$', PracticeTypeListView.as_view(),
        name='practice_types_list'),
    url(r'^facility_units/(?P<pk>[^/]+)/$',
        PracticeTypeDetailView.as_view(),
        name='practice_type_detail'),

    url(r'^specialities/$', SpecialityListView.as_view(),
        name='specialities_list'),
    url(r'^specialities/(?P<pk>[^/]+)/$',
        SpecialityDetailView.as_view(),
        name='speciality_detail'),

    url(r'^qualifications/$', QualificationListView.as_view(),
        name='qualifications_list'),
    url(r'^qualifications/(?P<pk>[^/]+)/$',
        QualificationDetailView.as_view(),
        name='qualification_detail'),

    url(r'^practitioners/$', PractitionerListView.as_view(),
        name='practitioners_list'),
    url(r'^practitioners/(?P<pk>[^/]+)/$',
        PractitionerDetailView.as_view(),
        name='practitioner_detail'),

    url(r'^practitioners_qualifications/$',
        PractitionerQualificationListView.as_view(),
        name='practitioner_qualifications_list'),
    url(r'^practitioners_qualifications/(?P<pk>[^/]+)/$',
        PractitionerQualificationDetailView.as_view(),
        name='practitioner_qualification_detail'),

    url(r'^practitioners_contacts/$', PractitionerContactListView.as_view(),
        name='practitioner_contacts_list'),
    url(r'^practitioners_contacts/(?P<pk>[^/]+)/$',
        PractitionerContactDetailView.as_view(),
        name='practitioner_contact_detail'),

    url(r'^practitioner_facilities/$', PractitionerFacilityListView.as_view(),
        name='practitioner_facilities_list'),
    url(r'^speciality/(?P<pk>[^/]+)/$',
        PractitionerFacilityDetailView.as_view(),
        name='practitioner_facility_detail')
)
