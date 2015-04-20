from django.core.urlresolvers import reverse

from model_mommy import mommy

from common.tests import ViewTestBase


from ..serializers import (
    PracticeTypeSerializer,
    SpecialitySerializer,
    QualificationSerializer,
    PractitionerSerializer,
    PractitionerQualificationSerializer,
    PractitionerContactSerializer,
    PractitionerFacilitySerializer,
)

from ..models import (
    PracticeType,
    Speciality,
    Qualification,
    Practitioner,
    PractitionerQualification,
    PractitionerContact,
    PractitionerFacility
)

test_views_config = [
    {
        'model': PracticeType,
        'list_url_name': 'practice_types_list',
        'detail_url_name': 'practice_type_detail',
        'serializer_cls': PracticeTypeSerializer
    },
    {
        'model': Speciality,
        'list_url_name': 'specialities_list',
        'detail_url_name': 'speciality_detail',
        'serializer_cls': SpecialitySerializer
    },
    {
        'model': Qualification,
        'list_url_name': 'qualifications_list',
        'detail_url_name': 'qualification_detail',
        'serializer_cls': QualificationSerializer
    },
    {
        'model': Practitioner,
        'list_url_name': 'practitioners_list',
        'detail_url_name': 'practitioner_detail',
        'serializer_cls': PractitionerSerializer
    },
    {
        'model': PractitionerQualification,
        'list_url_name': 'practitioner_qualifications_list',
        'detail_url_name': 'practitioner_qualification_detail',
        'serializer_cls': PractitionerQualificationSerializer
    },
    {
        'model': PractitionerContact,
        'list_url_name': 'practitioner_contacts_list',
        'detail_url_name': 'practitioner_contact_detail',
        'serializer_cls': PractitionerContactSerializer
    },
    {
        'model': PractitionerFacility,
        'list_url_name': 'practitioner_facilities_list',
        'detail_url_name': 'practitioner_facility_detail',
        'serializer_cls': PractitionerFacilitySerializer
    }
]


class TestViews(ViewTestBase):
    def setUp(self):
        self.base_namespace = 'api:facilities'
        super(TestViews, self).setUp()

    def test_list_endpoints(self):
        for test_config in test_views_config:
            model_cls = test_config.get('model')
            list_url_name = test_config.get('list_url_name')

            complete_list_url_name = self.base_namespace + ":{}".format(
                list_url_name)
            url = reverse(complete_list_url_name)

            mommy.make(model_cls)
            mommy.make(model_cls)

            response = self.client.get(url)

            response_data = self._dump_data_with_uuid_objects(response.data)
            self.assertEquals(2, response_data.get('count'))
            self.assertEquals(2, len(response_data.get('results')))
            self.assertEquals(200, response.status_code)
