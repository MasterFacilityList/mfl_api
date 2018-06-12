import json
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APITestCase
from model_mommy import mommy

from common.tests.test_views import (
    LoginMixin,
    default
)
from common.models import (
    Ward, UserCounty,
    County,
    Constituency,
    Contact,
    ContactType,
    UserConstituency,
    UserSubCounty,
    SubCounty)

from ..serializers import (
    OwnerSerializer,
    FacilitySerializer,
    FacilityDetailSerializer,
    FacilityStatusSerializer,
    FacilityUnitSerializer,
    FacilityListSerializer,
    FacilityOfficerSerializer,
    RegulatoryBodyUserSerializer,
    FacilityUnitRegulationSerializer,
    FacilityUpdatesSerializer
)
from ..models import (
    OwnerType,
    Owner,
    FacilityStatus,
    Facility,
    FacilityUnit,
    FacilityRegulationStatus,
    FacilityType,
    ServiceCategory,
    Service,
    Option,
    FacilityService,
    FacilityContact,
    FacilityOfficer,
    Officer,
    RegulatingBody,
    RegulatoryBodyUser,
    FacilityUnitRegulation,
    RegulationStatus,
    FacilityApproval,
    FacilityUpdates,
    KephLevel,
    FacilityLevelChangeReason
)

from django.contrib.auth.models import Group, Permission


class TestGroupAndPermissions(object):

    def setUp(self):
        super(TestGroupAndPermissions, self).setUp()
        self.view_unpublished_perm = Permission.objects.get(
            codename="view_unpublished_facilities")
        self.view_approved_perm = Permission.objects.get(
            codename="view_unapproved_facilities")
        self.view_classified_perm = Permission.objects.get(
            codename="view_classified_facilities")
        self.public_group = mommy.make(Group, name="public")
        self.admin_group = mommy.make(Group, name="mfl admins")
        self.admin_group.permissions.add(self.view_unpublished_perm.id)
        self.admin_group.permissions.add(self.view_approved_perm.id)
        self.admin_group.permissions.add(self.view_classified_perm.id)


def load_dump(x, *args, **kwargs):
    return json.loads(json.dumps(x, *args, **kwargs))


class TestOwnersView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestOwnersView, self).setUp()
        self.url = reverse('api:facilities:owners_list')

    def test_list_owners(self):
        ownertype = mommy.make(OwnerType)
        owner_1 = mommy.make(Owner, owner_type=ownertype)
        owner_2 = mommy.make(Owner, owner_type=ownertype)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                OwnerSerializer(
                    owner_2,
                    context={
                        'request': response.request
                    }
                ).data,
                OwnerSerializer(
                    owner_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_post(self):
        owner_type = mommy.make(OwnerType)

        data = {

            "name": "Ministry of Health",
            "description": "This is the minisrry of health Kenya",
            "abbreviation": "MOH",
            "owner_type": owner_type.id
        }
        response = self.client.post(self.url, data)
        response_data = json.dumps(response.data, default=default)
        self.assertEquals(201, response.status_code)
        self.assertIn("id", response_data)
        self.assertIn("code", response_data)
        self.assertIn("name", response_data)
        self.assertIn("description", response_data)
        self.assertIn("abbreviation", response_data)
        self.assertIn("owner_type", response_data)
        self.assertEquals(1, Owner.objects.count())

    def test_retrive_single_owner(self):
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        url = self.url + "{}/".format(owner.id)
        response = self.client.get(url)
        expected_data = OwnerSerializer(
            owner,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data, default=default),
            load_dump(response.data, default=default)
        )

    def test_filtering(self):
        owner_type_1 = mommy.make(OwnerType)
        owner_type_2 = mommy.make(OwnerType)
        owner_1 = mommy.make(Owner, name='CHAK', owner_type=owner_type_1)
        owner_2 = mommy.make(Owner, name='MOH', owner_type=owner_type_1)
        owner_3 = mommy.make(Owner, name='Private', owner_type=owner_type_2)

        self.maxDiff = None
        url = self.url + "?owner_type={}".format(owner_type_1.id)
        response_1 = self.client.get(url)
        expected_data_1 = {
            "results": [
                # Due to ordering in view CHAK will always be first
                OwnerSerializer(
                    owner_2,
                    context={
                        'request': response_1.request
                    }
                ).data,
                OwnerSerializer(
                    owner_1,
                    context={
                        'request': response_1.request
                    }
                ).data
            ]
        }

        self.assertEquals(200, response_1.status_code)
        self.assertEquals(
            load_dump(expected_data_1['results'], default=default),
            load_dump(response_1.data['results'], default=default)
        )

        url = self.url + "?owner_type={}".format(owner_type_2.id)
        response_2 = self.client.get(url)
        expected_data_2 = {
            "results": [
                OwnerSerializer(
                    owner_3,
                    context={
                        'request': response_2.request
                    }
                ).data
            ]
        }

        self.assertEquals(200, response_2.status_code)
        self.assertEquals(
            load_dump(expected_data_2['results'], default=default),
            load_dump(response_2.data['results'], default=default)
        )


class TestFacilityView(LoginMixin, TestGroupAndPermissions, APITestCase):

    def setUp(self):
        super(TestFacilityView, self).setUp()
        self.url = reverse('api:facilities:facilities_list')

    def test_facility_listing(self):
        facility_1 = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        facility_3 = mommy.make(Facility)

        response = self.client.get(self.url)
        expected_data = {
            "results": [
                FacilitySerializer(
                    facility_3,
                    context={
                        'request': response.request
                    }
                ).data,
                FacilitySerializer(
                    facility_2,
                    context={
                        'request': response.request
                    }
                ).data,
                FacilitySerializer(
                    facility_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_facilties_that_need_regulation_or_not(self):
        facility_1 = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(Facility)
        mommy.make(
            FacilityRegulationStatus, facility=facility_1)
        mommy.make(
            FacilityRegulationStatus, facility=facility_2)

        url = self.url + "?regulated=true"

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        # 2 facilities are not regulated
        self.assertEquals(2, response.data.get("count"))
        self.assertEquals(2, len(response.data.get("results")))
        # get unregulated
        url = self.url + "?regulated=false"
        response_2 = self.client.get(url)

        self.assertEquals(200, response_2.status_code)
        self.assertEquals(1, response_2.data.get("count"))
        # only one facility is not regulated
        self.assertEquals(1, len(response_2.data.get("results")))

    def test_retrieve_facility(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/".format(facility.id)
        response = self.client.get(url)
        expected_data = FacilityDetailSerializer(
            facility,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data, default=default),
            load_dump(response.data, default=default)
        )

    def test_get_facility_services(self):
        facility = mommy.make(Facility, name='thifitari')
        service_category = mommy.make(ServiceCategory, name='a good service')
        service = mommy.make(Service, name='savis', category=service_category)
        option = mommy.make(
            Option, option_type='BOOLEAN', display_text='Yes/No')
        facility_service = mommy.make(
            FacilityService, facility=facility, service=service, option=option)
        expected_data = [
            {
                "id": facility_service.id,
                "service_id": service.id,
                "service_name": service.name,
                "option_name": option.display_text,
                "option": str(option.id),
                "category_name": service_category.name,
                "category_id": service_category.id,
                "average_rating": facility_service.average_rating,
                "number_of_ratings": 0,
                "service_code": service.code
            }
        ]
        url = self.url + "{}/".format(facility.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        facility_services = response.data.get('facility_services')
        self.assertEquals(expected_data, facility_services)

    def test_filter_facilities_by_many_service_categories(self):
        category = mommy.make(ServiceCategory)
        category_2 = mommy.make(ServiceCategory)
        mommy.make(ServiceCategory)
        service = mommy.make(Service, category=category)
        option = mommy.make(Option)
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        service_x = mommy.make(Service)
        service_y = mommy.make(Service)
        mommy.make(FacilityService, facility=facility_2, service=service_x)

        service_2 = mommy.make(Service, category=category_2)
        mommy.make(FacilityService, facility=facility_2, service=service_y)
        mommy.make(
            FacilityService, facility=facility, option=option, service=service)
        mommy.make(
            FacilityService, facility=facility,
            option=option, service=service_2)

        url = self.url + "?service_category={},{}".format(
            category.id, category_2.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [FacilitySerializer(facility).data]
        }
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_filter_facilities_by_one_category(self):
        category = mommy.make(ServiceCategory)
        mommy.make(ServiceCategory)
        service = mommy.make(Service, category=category)
        option = mommy.make(Option)
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        service_x = mommy.make(Service)
        service_y = mommy.make(Service)
        mommy.make(FacilityService, facility=facility_2, service=service_x)
        mommy.make(FacilityService, facility=facility_2, service=service_y)
        mommy.make(
            FacilityService, facility=facility, option=option, service=service)

        url = self.url + "?service_category={}".format(
            category.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [FacilitySerializer(facility).data]
        }
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_filter_facilities_by_many_service_categories_no_data(self):
        category = mommy.make(ServiceCategory)
        category_2 = mommy.make(ServiceCategory)
        # this category is unlinked thus there is no facility
        # service linked to the category
        category_3 = mommy.make(ServiceCategory)
        mommy.make(ServiceCategory)
        service = mommy.make(Service, category=category)
        option = mommy.make(Option)
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        service_x = mommy.make(Service)
        service_y = mommy.make(Service)
        mommy.make(FacilityService, facility=facility_2, service=service_x)

        service_2 = mommy.make(Service, category=category_2)
        mommy.make(FacilityService, facility=facility_2, service=service_y)
        mommy.make(
            FacilityService, facility=facility, option=option, service=service)
        mommy.make(
            FacilityService, facility=facility, option=option,
            service=service_2)

        url = self.url + "?service_category={},{},{}".format(
            category.id, category_2.id, category_3.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [FacilitySerializer(facility).data]
        }
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_facility_slimmed_down_listing(self):
        url = reverse("api:facilities:facilities_read_list")
        facility = mommy.make(Facility)
        response = self.client.get(url)
        expected_data = {
            "results": [
                FacilityListSerializer(
                    facility,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }

        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_get_approved_facilities(self):
        self.maxDiff = None
        self.user.is_national = True
        self.user.is_superuser = True
        self.user.save()
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        url = self.url + "?is_approved=true"
        response_1 = self.client.get(url)
        expected_data_1 = {
            "results": [
                FacilitySerializer(
                    facility,
                    context={
                        'request': response_1.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response_1.status_code)
        self.assertEquals(
            load_dump(expected_data_1['results'], default=default),
            load_dump(response_1.data['results'], default=default)
        )

        url = self.url + "?is_approved=false"
        response_2 = self.client.get(url)
        expected_data_2 = {
            "results": [
                FacilitySerializer(
                    facility_2,
                    context={
                        'request': response_2.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response_1.status_code)
        self.assertEquals(
            expected_data_2['results'], response_2.data['results']
        )

    def test_get_facility_as_regulator(self):
        self.client.logout()
        user = mommy.make(get_user_model())
        reg_body = mommy.make(RegulatingBody)
        mommy.make(RegulatoryBodyUser, user=user, regulatory_body=reg_body)
        self.assertIsNotNone(user.regulator)
        self.client.force_authenticate(user)
        user.groups.add(self.admin_group)

        facility = mommy.make(Facility, regulatory_body=reg_body)
        mommy.make(Facility)
        response = self.client.get(self.url)

        self.assertEquals(200, response.status_code)
        self.assertEquals(facility, Facility.objects.get(
            id=response.data['results'][0].get("id")))

    def test_get_facility_as_an_anonymous_user(self):
        self.client.logout()
        self.client.get(self.url)

    def test_patch_facility(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        url = self.url + "{}/".format(facility.id)
        data = {
            "name": "A new name"
        }
        response = self.client.patch(url, data)
        # error the reponse status code us not appearing as a 204
        self.assertEquals(200, response.status_code)
        facility_retched = Facility.objects.get(id=facility.id)
        self.assertEquals(facility.name, facility_retched.name)

    def test_get_facilities_with_unacked_updates(self):
        true_url = self.url + "?has_edits=true"
        false_url = self.url + "?has_edits=false"
        facility_a = mommy.make(
            Facility, id='67105b48-0cc0-4de2-8266-e45545f1542f')
        mommy.make(FacilityApproval, facility=facility_a)
        facility_a.name = 'jina ingine'
        facility_a.save()
        facility_b = mommy.make(Facility)
        facility_a_refetched = Facility.objects.get(
            id='67105b48-0cc0-4de2-8266-e45545f1542f')
        true_response = self.client.get(true_url)
        true_expected_data = {
            "results": [
                FacilitySerializer(
                    facility_a_refetched,
                    context={
                        'request': true_response.request
                    }
                ).data
            ]
        }
        false_response = self.client.get(false_url)
        false_expected_data = {
            "results": [
                FacilitySerializer(
                    facility_b,
                    context={
                        'request': false_response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, true_response.status_code)
        self.assertEquals(
            load_dump(true_expected_data['results'], default=default),
            load_dump(true_response.data['results'], default=default)
        )
        self.assertEquals(200, true_response.status_code)
        self.assertEquals(
            load_dump(false_expected_data['results'], default=default),
            load_dump(false_response.data['results'], default=default)
        )

    def test_partial_response_on_list_endpoint(self):
        url = self.url + "?fields=id,name"
        facility = mommy.make(Facility)
        response = self.client.get(url)
        self.assertEquals(
            [
                {
                    "id": str(facility.id),
                    "name": facility.name
                }
            ],
            response.data.get("results"))

    def test_partial_response_on_get_single_endpoint(self):
        facility = mommy.make(Facility)
        url = self.url + "{}/?fields=id,name".format(str(facility.id))
        response = self.client.get(url)
        self.assertEquals(
            {
                "id": str(facility.id),
                "name": facility.name
            },
            response.data
        )

    def test_filter_facilities_by_sub_counties(self):
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        sub_county = mommy.make(SubCounty, county=county)
        ward = mommy.make(Ward, sub_county=sub_county, constituency=const)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility, _quantity=5)

        # too lazy to bootstrap the entire facility workflow thus the superuser
        nat_user = mommy.make(
            get_user_model(), is_national=True, is_superuser=True)
        county_user = mommy.make(get_user_model(), is_superuser=True)
        mommy.make(UserCounty, county=county, user=county_user)
        const_user = mommy.make(get_user_model(), is_superuser=True)
        mommy.make(
            UserConstituency, user=const_user, constituency=const,
            created_by=county_user, updated_by=county_user
        )
        sub_county_user = mommy.make(get_user_model(), is_superuser=True)
        mommy.make(
            UserSubCounty, user=sub_county_user, sub_county=sub_county)

        sub_county_const_user = mommy.make(
            get_user_model(), is_superuser=True)
        mommy.make(
            UserConstituency, user=sub_county_const_user, constituency=const,
            created_by=county_user, updated_by=county_user)

        # nation user should see all facilities
        self.client.force_authenticate(nat_user)
        url = reverse("api:facilities:facilities_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(6, response.data.get('count'))
        self.client.logout()

        # county user should see facilities in county
        self.client.force_authenticate(county_user)
        url = reverse("api:facilities:facilities_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.client.logout()

        # constituencies user should see facilities in constituencies
        self.client.force_authenticate(county_user)
        url = reverse("api:facilities:facilities_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.client.logout()

        # sub-county user should see facilities in sub-counties
        self.client.force_authenticate(county_user)
        url = reverse("api:facilities:facilities_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.client.logout()

        # A user assigned to  both sub-county and constituency should see
        # facilities in sub-county
        self.client.force_authenticate(sub_county_const_user)
        url = reverse("api:facilities:facilities_list")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.client.logout()


class CountyAndNationalFilterBackendTest(APITestCase):

    def setUp(self):
        password = 'mtihani123'
        self.user = get_user_model().objects.create_superuser(
            email='tester@ehealth.or.ke',
            first_name='Test',
            username='test',
            employee_number='1241414141',
            password=password,
            is_national=False
        )
        self.user_county = mommy.make(UserCounty, user=self.user)
        self.client.login(email='tester@ehealth.or.ke', password=password)
        self.maxDiff = None
        self.url = reverse('api:facilities:facilities_list')
        super(CountyAndNationalFilterBackendTest, self).setUp()

    def test_facility_county_national_filter_backend(self):
        """Testing the filtered by county level"""
        mommy.make(Facility)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        # The response should be filtered out for this user; not national
        self.assertEquals(len(response.data["results"]), 0)


class TestFacilityStatusView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestFacilityStatusView, self).setUp()
        self.url = reverse("api:facilities:facility_statuses_list")

    def test_list_facility_status(self):
        status_1 = mommy.make(FacilityStatus, name='OPERTATIONAL')
        status_2 = mommy.make(FacilityStatus, name='NON_OPERATIONAL')
        status_3 = mommy.make(FacilityStatus, name='CLOSED')
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                FacilityStatusSerializer(
                    status_3,
                    context={
                        'request': response.request
                    }
                ).data,
                FacilityStatusSerializer(
                    status_2,
                    context={
                        'request': response.request
                    }
                ).data,
                FacilityStatusSerializer(
                    status_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_retrieve_facility_status(self):
        status = mommy.make(FacilityStatus, name='OPERTATIONAL')
        url = self.url + "{}/".format(status.id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.data,
            FacilityStatusSerializer(
                status,
                context={
                    'request': response.request
                }
            ).data
        )


class TestFacilityUnitView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestFacilityUnitView, self).setUp()
        self.url = reverse("api:facilities:facility_units_list")

    def test_list_facility_units(self):
        unit_1 = mommy.make(FacilityUnit)
        unit_2 = mommy.make(FacilityUnit)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                FacilityUnitSerializer(
                    unit_2,
                    context={
                        'request': response.request
                    }
                ).data,
                FacilityUnitSerializer(
                    unit_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data['results'], default=default),
            load_dump(response.data['results'], default=default)
        )

    def test_retrieve_facility_unit(self):
        unit = mommy.make(FacilityUnit)
        url = self.url + "{}/".format(unit.id)
        response = self.client.get(url)
        expected_data = FacilityUnitSerializer(
            unit,
            context={
                'request': response.request
            }
        ).data

        self.assertEquals(200, response.status_code)
        self.assertEquals(
            load_dump(expected_data, default=default),
            load_dump(response.data, default=default)
        )


class TestInspectionAndCoverReportsView(LoginMixin, APITestCase):

    def test_inspection_report(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_inspection_report',
            kwargs={'pk': facility.id})

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'inspection_report.txt')

    def test_cover_reports(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_cover_report',
            kwargs={'pk': facility.id})

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'cover_report.html')

    def test_correction_templates(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_correction_template',
            kwargs={'pk': facility.id})

        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'correction_template.html')

    def test_facility_detail_with_permission(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_detail_report',
            kwargs={'pk': facility.id}
        )
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'facility_details.html')

    def test_facility_detail_without_permission(self):
        ward = mommy.make(Ward)
        facility = mommy.make(Facility, ward=ward)
        url = reverse(
            'api:facilities:facility_detail_report',
            kwargs={'pk': facility.id}
        )
        get_user_model().objects.create_user(
            email='noperms@domain.com',
            password='password1',
            first_name='fname',
            employee_number='enum'
        )
        client = self.client.__class__()
        self.assertTrue(
            client.login(email='noperms@domain.com', password='password1')
        )
        response = client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'facility_details.html')


class TestDashBoardView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestDashBoardView, self).setUp()
        self.url = reverse('api:facilities:dashboard')
        county = mommy.make(County, name='Kiambu')
        mommy.make(UserCounty, county=county, user=self.user)

    def _equate_json(self, payload):
        return json.loads(json.dumps(payload))

    def test_get_dashboard_national_user(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        sub_county = mommy.make(SubCounty, county=county)
        ward = mommy.make(
            Ward, constituency=constituency, sub_county=sub_county)
        facility_type = mommy.make(FacilityType)
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        status = mommy.make(FacilityStatus)
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,

        )
        self.assertEquals(1, Facility.objects.count())
        expected_data = {
            "owners_summary": [
                {
                    "count": 1,
                    "name": owner.name
                },
            ],
            "pending_updates": 1,
            "recently_created": 1,
            "county_summary": [
                {
                    "count": 1,
                    "name": str(county.name),
                    "chu_count": 0
                },
                # the county belonging to the logged in user
                {
                    "count": 0,
                    "name": "Kiambu",
                    "chu_count": 0
                },
            ],
            "wards_summary": [],
            "total_facilities": 1,
            "status_summary": [
                {
                    "count": 1,
                    "name": str(status.name)
                },
            ],
            "owner_types": [
                {
                    "count": 1,
                    "name": str(owner_type. name)
                },
            ],
            "constituencies_summary": [],
            "types_summary": [
                {
                    "count": 1,
                    "name": str(facility_type.name)
                },
            ],
            "rejected_facilities_count": 0,
            "recently_created_chus": 0,
            "closed_facilities_count": 0,
            "rejected_chus": 0,
            "chus_pending_approval": 0,
            "total_chus": 0
        }
        response = self.client.get(self.url)

        self.assertAlmostEquals(
            self._equate_json(expected_data),
            self._equate_json(response.data))

    def test_get_dashboard_as_county_user(self):
        # remove the user as a national user
        self.user.is_national = False
        self.user.save()
        constituency = mommy.make(
            Constituency, county=self.user.county)
        sub_county = mommy.make(SubCounty, county=self.user.county)
        ward = mommy.make(
            Ward, constituency=constituency, sub_county=sub_county)
        facility_type = mommy.make(FacilityType)
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        status = mommy.make(FacilityStatus)
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,

        )
        expected_data = {
            "owners_summary": [
                {
                    "count": 1,
                    "name": owner.name
                },
            ],
            "pending_updates": 1,
            "recently_created": 1,
            "county_summary": [],
            "wards_summary": [],
            "total_facilities": 1,
            "status_summary": [
                {
                    "count": 1,
                    "name": status.name
                },
            ],
            "owner_types": [
                {
                    "count": 1,
                    "name": owner_type. name
                },
            ],
            "constituencies_summary": [
                {
                    "name": str(sub_county.name),
                    "count": 1,
                    "chu_count": 0
                }
            ],
            "types_summary": [
                {
                    "count": 1,
                    "name": facility_type.name
                },
            ],
            "rejected_facilities_count": 0,
            "recently_created_chus": 0,
            "closed_facilities_count": 0,
            "rejected_chus": 0,
            "chus_pending_approval": 0,
            "total_chus": 0
        }
        response = self.client.get(self.url)
        self.assertEquals(
            self._equate_json(expected_data),
            self._equate_json(response.data))

    def test_get_dashboard_as_sub_county_user(self):
        # ensure user has all facilities to see facilities
        facility_perms = Permission.objects.filter(
            codename__icontains='facility')
        facility_perms_2 = Permission.objects.filter(
            codename__icontains='facilities')
        user = mommy.make(get_user_model())
        for perm in facility_perms:
            user.permissions.add(perm)
        for perm in facility_perms_2:
            user.permissions.add(perm)
        self.user.is_national = False

        self.user.save()
        constituency = mommy.make(
            Constituency, county=self.user.county)
        sub_county = mommy.make(SubCounty, county=self.user.county)
        ward = mommy.make(
            Ward, constituency=constituency, sub_county=sub_county)
        facility_type = mommy.make(FacilityType)
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        status = mommy.make(FacilityStatus)
        mommy.make(
            UserConstituency, created_by=self.user, updated_by=self.user,
            user=user, constituency=constituency)
        mommy.make(
            UserSubCounty, created_by=self.user, updated_by=self.user,
            user=user, sub_county=sub_county)
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,

        )
        self.client.force_authenticate(user)
        user.is_superuser = True
        user.save()
        expected_data = {
            "owners_summary": [
                {
                    "count": 1,
                    "name": str(owner.name)
                },
            ],
            "pending_updates": 1,
            "recently_created": 1,
            "county_summary": [],
            "wards_summary": [
                {
                    "name": str(ward.name),
                    "count": 1,
                    "chu_count": 0
                }
            ],
            "total_facilities": 1,
            "status_summary": [
                {
                    "count": 1,
                    "name": str(status.name)
                },
            ],
            "owner_types": [
                {
                    "count": 1,
                    "name": str(owner_type. name)
                },
            ],
            "constituencies_summary": [],
            "types_summary": [
                {
                    "count": 1,
                    "name": str(facility_type.name)
                },
            ],
            "rejected_facilities_count": 0,
            "recently_created_chus": 0,
            "closed_facilities_count": 0,
            "rejected_chus": 0,
            "chus_pending_approval": 0,
            "total_chus": 0
        }
        response = self.client.get(self.url)

        self.assertEquals(
            self._equate_json(expected_data),
            self._equate_json(response.data))

    def test_get_dashboard_user_has_no_role(self):
        user = mommy.make(get_user_model())
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

    def test_created_last_one_week_param(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        facility_type = mommy.make(FacilityType)
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        status = mommy.make(FacilityStatus)
        right_now = timezone.now()
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=10)

        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=3)

        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now
        )
        url = self.url + "?last_week=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.data.get("recently_created"), 2)

    def test_created_last_one_month_param(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        facility_type = mommy.make(FacilityType)
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        status = mommy.make(FacilityStatus)
        right_now = timezone.now()
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=10)

        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=3)

        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now
        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=35)
        )
        url = self.url + "?last_month=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.data.get("recently_created"), 3)

    def test_created_last_one_quarter_param(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        mommy.make(SubCounty, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        facility_type = mommy.make(FacilityType)
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        status = mommy.make(FacilityStatus)
        right_now = timezone.now()
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=10)

        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=3)

        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now
        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=100)
        )
        url = self.url + "?last_three_months=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.data.get("recently_created"), 3)

    def test_fields_response(self):
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        sub_county = mommy.make(SubCounty, county=county)
        ward = mommy.make(
            Ward, constituency=constituency, sub_county=sub_county)
        facility_type = mommy.make(FacilityType)
        owner_type = mommy.make(OwnerType)
        owner = mommy.make(Owner, owner_type=owner_type)
        status = mommy.make(FacilityStatus)
        right_now = timezone.now()
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=10)
        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=3)
        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now
        )
        mommy.make(
            Facility,
            ward=ward,
            facility_type=facility_type,
            owner=owner,
            operation_status=status,
            created=right_now - timedelta(days=100)
        )
        url = self.url + "?quarterly=true&fields=recently_created"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.data, {"recently_created": 3})


class TestFacilityContactView(LoginMixin, APITestCase):

    def test_list_facility_contacts(self):
        url = reverse('api:facilities:facility_contacts_list')
        facility = mommy.make(Facility)
        contact_type = mommy.make(ContactType, name='EMAIL')
        contact = mommy.make(
            Contact, contact_type=contact_type, contact='0700000000')
        fc = mommy.make(
            FacilityContact, contact=contact, facility=facility)
        single_url = url + "{}/".format(fc.id)
        response = self.client.get(single_url)
        self.assertEquals(200, response.status_code)
        self.assertEquals('EMAIL', response.data.get('contact_type'))
        self.assertEquals('0700000000', response.data.get('actual_contact'))


class TestFacilityOfficerView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestFacilityOfficerView, self).setUp()
        self.url = reverse('api:facilities:facility_officers_list')

    def test_list_facility_officers(self):
        facility_officer = mommy.make(FacilityOfficer)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                FacilityOfficerSerializer(
                    facility_officer,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.assertEquals(expected_data['results'], response.data['results'])

    def test_retrive_single_facility_officer(self):
        facility_officer = mommy.make(FacilityOfficer)
        url = self.url + "{}/".format(facility_officer.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(str(facility_officer.id), response.data.get('id'))

    def test_post(self):
        facility = mommy.make(Facility)
        officer = mommy.make(Officer)
        data = {
            "facility": str(facility.id),
            "officer": str(officer.id)
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, FacilityOfficer.objects.count())


class TestRegulatoryBodyUserView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestRegulatoryBodyUserView, self).setUp()
        self.url = reverse("api:facilities:regulatory_body_users_list")

    def test_listing(self):
        reg_bod_user = mommy.make(RegulatoryBodyUser)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [
                RegulatoryBodyUserSerializer(
                    reg_bod_user,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(expected_data['results'], response.data['results'])

    def test_retrieving_single_record(self):
        reg_bod_user = mommy.make(RegulatoryBodyUser)
        url = self.url + "{}/".format(reg_bod_user.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = RegulatoryBodyUserSerializer(
            reg_bod_user,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(expected_data, response.data)

    def test_posting(self):
        reg_body = mommy.make(RegulatingBody)
        user = mommy.make(get_user_model())
        data = {
            "regulatory_body": reg_body.id,
            "user": user.id
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertIn('id', response.data)
        self.assertEquals(1, RegulatingBody.objects.count())


class TestFacilityRegulator(TestGroupAndPermissions, APITestCase):

    def test_filtering_facilities_by_regulator(self):
        url = reverse("api:facilities:facilities_list")
        reg_body = mommy.make(RegulatingBody)
        user = mommy.make(get_user_model(), password='test123456')
        user.groups.add(self.admin_group)
        mommy.make(RegulatoryBodyUser, user=user, regulatory_body=reg_body)
        facility = mommy.make(Facility, regulatory_body=reg_body)
        self.client.force_authenticate(user)
        mommy.make(Facility)
        response = self.client.get(url)

        self.assertEquals(facility, Facility.objects.get(
            id=response.data['results'][0].get("id")))
        self.assertEquals(200, response.status_code)


class TestFacilityUnitRegulationView(LoginMixin, APITestCase):

    def setUp(self):
        super(TestFacilityUnitRegulationView, self).setUp()
        self.url = reverse("api:facilities:facility_unit_regulations_list")

    def test_listing(self):
        obj_1 = mommy.make(FacilityUnitRegulation)
        obj_2 = mommy.make(FacilityUnitRegulation)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [
                FacilityUnitRegulationSerializer(
                    obj_2,
                    context={
                        'request': response.request
                    }
                ).data,
                FacilityUnitRegulationSerializer(
                    obj_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(expected_data['results'], response.data['results'])

    def test_retrieve_single_record(self):
        obj = mommy.make(FacilityUnitRegulation)
        url = self.url + "{}/".format(obj.id)
        response = self.client.get(url)
        expected_data = FacilityUnitRegulationSerializer(
            obj,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(200, response.status_code)
        self.assertEquals(expected_data, response.data)

    def test_posting(self):
        facility_unit = mommy.make(FacilityUnit)
        reg_status = mommy.make(RegulationStatus)
        data = {
            "facility_unit": str(facility_unit.id),
            "regulation_status": str(reg_status.id)
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertIn('id', response.data)


class TestFacilityUpdates(LoginMixin, APITestCase):

    def setUp(self):
        super(TestFacilityUpdates, self).setUp()
        self.url = reverse('api:facilities:facility_updatess_list')

    def test_listing(self):
        update = [
            {
                "actual_value": "Some name",
                "display_value": "Some name",
                "field_name": "name",
                "human_field_name": "name"
            }
        ]
        obj = mommy.make(
            FacilityUpdates, facility_updates=json.dumps(update))
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        expected_data = {
            "results": [
                FacilityUpdatesSerializer(
                    obj,
                    context={
                        'request': response.request
                    }
                ).data

            ]
        }
        self.assertEquals(expected_data['results'], response.data['results'])

    def test_retrieving(self):
        update = [
            {
                "actual_value": "Some name",
                "display_value": "Some name",
                "field_name": "name",
                "human_field_name": "name"
            }
        ]
        obj = mommy.make(
            FacilityUpdates, facility_updates=json.dumps(update))
        url = self.url + "{}/".format(obj.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_data = FacilityUpdatesSerializer(
            obj,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(expected_data, response.data)

    def test_approving(self):
        facility = mommy.make(
            Facility,
            id='67105b48-0cc0-4de2-8266-e45545f1542f')
        mommy.make(FacilityApproval, facility=facility)
        obj = mommy.make(
            FacilityUpdates,
            facility=facility,
            facility_updates=json.dumps([
                {
                    "actual_value": "jina",
                    "display_value": "jina",
                    "field_name": "name",
                    "human_field_name": "name"
                }
            ]))
        facility_refetched = Facility.objects.get(
            id='67105b48-0cc0-4de2-8266-e45545f1542f')
        self.assertTrue(facility_refetched.has_edits)
        self.assertEquals(facility_refetched.latest_update, str(obj.id))
        url = self.url + "{}/".format(obj.id)
        data = {"approved": True}
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        obj_refetched = Facility.objects.get(
            id='67105b48-0cc0-4de2-8266-e45545f1542f')
        self.assertFalse(obj_refetched.has_edits)
        self.assertIsNone(obj_refetched.latest_update)
        self.assertTrue(response.data.get('approved'))
        self.assertEquals('jina', obj_refetched.name)
        facility_updates_refetched = FacilityUpdates.objects.get(id=obj.id)
        expected_data = FacilityUpdatesSerializer(
            facility_updates_refetched,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(
            load_dump(expected_data, default=default),
            load_dump(response.data, default=default)
        )

    def test_cancelling(self):
        facility = mommy.make(
            Facility,
            id='67105b48-0cc0-4de2-8266-e45545f1542f')
        obj = mommy.make(
            FacilityUpdates,
            facility=facility,
            facility_updates=json.dumps([
                {
                    "actual_value": "jina",
                    "display_value": "jina",
                    "field_name": "name",
                    "human_field_name": "name"
                }
            ]
            ))
        url = self.url + "{}/".format(obj.id)
        data = {"cancelled": True}
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        obj_refetched = Facility.objects.get(
            id='67105b48-0cc0-4de2-8266-e45545f1542f')
        self.assertFalse(response.data.get('approved'))
        self.assertTrue(response.data.get('cancelled'))
        self.assertNotEquals('jina', obj_refetched.name)


class TestFacilityConsituencyUserFilter(TestGroupAndPermissions, APITestCase):

    def test_filter_by_constituency(self):
        user = mommy.make(get_user_model())
        user_2 = mommy.make(get_user_model())
        county = mommy.make(County)
        mommy.make(UserCounty, user=user_2, county=county)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        facility = mommy.make(Facility, ward=ward)
        mommy.make(Facility)
        mommy.make(
            UserConstituency, user=user, constituency=constituency,
            created_by=user_2, updated_by=user_2)
        url = reverse("api:facilities:facilities_list")
        self.client.force_authenticate(user)
        user.groups.add(self.admin_group)
        response = self.client.get(url)
        self.assertEquals(facility, Facility.objects.get(
            id=response.data['results'][0].get("id")))


class TestFilterRejectedFacilities(LoginMixin, APITestCase):
    def test_filter_rejected_facilities(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility_2 = mommy.make(Facility)
        mommy.make(FacilityApproval, is_cancelled=True, facility=facility_2)
        url = reverse("api:facilities:facilities_list")
        url = url + "?rejected=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get("count"))
        expected_data = [FacilitySerializer(
            facility_2,
            context={
                'request': response.request
            }
        ).data]

        self.assertEquals(
            load_dump(expected_data, default=default),
            load_dump(response.data['results'], default=default)
        )


class TestKephLevel(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:keph_levels_list")
        super(TestKephLevel, self).setUp()

    def test_listing(self):
        mommy.make(KephLevel)
        mommy.make(KephLevel)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get("count"))

    def test_retrieving_single_record(self):
        keph = mommy.make(KephLevel)
        url = self.url + "{}/".format(str(keph.id))
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_posting(self):
        data = {
            "name": "level 1"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)

    def test_updating(self):
        keph = mommy.make(KephLevel)
        data = {
            "name": "an awesome name"
        }
        url = self.url + "{}/".format(str(keph.id))
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        keph_refetched = KephLevel.objects.get(id=keph.id)
        self.assertEquals("an awesome name", keph_refetched.name)


class TestFacilityLevelChangeReasonView(LoginMixin, APITestCase):
    def setUp(self):
        super(TestFacilityLevelChangeReasonView, self).setUp()
        self.url = reverse("api:facilities:facility_level_change_reasons_list")

    def test_post(self):
        data = {
            "reason": "This is a reason",
            "description": "The description of the reason"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, FacilityLevelChangeReason.objects.count())

    def test_listing(self):
        mommy.make(FacilityLevelChangeReason)
        mommy.make(FacilityLevelChangeReason)
        mommy.make(FacilityLevelChangeReason)
        mommy.make(FacilityLevelChangeReason)
        mommy.make(FacilityLevelChangeReason)
        self.assertEquals(5, FacilityLevelChangeReason.objects.count())
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get('count'))
        self.assertEquals(5, len(response.data.get('results')))

    def test_restrieving(self):
        reason_1 = mommy.make(FacilityLevelChangeReason)
        mommy.make(FacilityLevelChangeReason)
        self.assertEquals(2, FacilityLevelChangeReason.objects.count())
        url = self.url + "{}/".format(reason_1.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(str(reason_1.id), response.data.get("id"))

    def test_updating(self):
        reason = mommy.make(FacilityLevelChangeReason)
        data = {
            "reason": "reason edited"
        }
        url = self.url + "{}/".format(reason.id)
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        reason_refetched = FacilityLevelChangeReason.objects.get(id=reason.id)
        self.assertEquals(reason_refetched.reason, data.get("reason"))


class TestRegulatoryBodyContacts(LoginMixin, APITestCase):
    def setUp(self):
        super(TestRegulatoryBodyContacts, self).setUp()

    def test_save(self):
        url = reverse("api:facilities:regulating_bodies_list")
        reg_status = mommy.make(RegulationStatus)
        data = {
            "name": "this is a reg body",
            'regulation_verb': 'REGISTER',
            'default_status': str(reg_status.id),
            "contacts": [
                {
                    "contact": "jina@mail.com",
                    "contact_type": mommy.make(ContactType, name="EAMIL").id
                }
            ]
        }
        response = self.client.post(url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, RegulatingBody.objects.count())
        self.assertEquals(1, Contact.objects.count())

    def test_save_errors(self):
        url = reverse("api:facilities:regulating_bodies_list")
        reg_status = mommy.make(RegulationStatus)
        data = {
            "name": "this is a reg body",
            'regulation_verb': 'REGISTER',
            'default_status': str(reg_status.id),
            "contacts": [
                {
                    "contact": "jina@mail.com"
                }
            ]
        }
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, RegulatingBody.objects.count())
        self.assertEquals(0, Contact.objects.count())

    def test_save_contact_missing(self):
        url = reverse("api:facilities:regulating_bodies_list")
        reg_status = mommy.make(RegulationStatus)
        data = {
            "name": "this is a reg body",
            'regulation_verb': 'REGISTER',
            'default_status': str(reg_status.id),
            "contacts": [
                {
                }
            ]
        }
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, RegulatingBody.objects.count())
        self.assertEquals(0, Contact.objects.count())

    def test_save_contact_type_invalid(self):
        url = reverse("api:facilities:regulating_bodies_list")
        contact_type = mommy.make(ContactType, name="EAMIL")
        contact_type_id = contact_type.id
        contact_type.delete()
        reg_status = mommy.make(RegulationStatus)
        data = {
            "name": "this is a reg body",
            'regulation_verb': 'REGISTER',
            'default_status': str(reg_status.id),
            "contacts": [
                {
                    "contact": "jina@mail.com",
                    "contact_type": contact_type_id
                }
            ]
        }
        response = self.client.post(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, RegulatingBody.objects.count())
        self.assertEquals(0, Contact.objects.count())

    def test_upate_contact_type_valid(self):
        url = reverse("api:facilities:regulating_bodies_list")
        reg_body = mommy.make(RegulatingBody)
        url = url + "{}/".format(reg_body.id)
        contact_type = mommy.make(ContactType)
        data = {
            "contacts": [
                {
                    "contact": "jina@mail.com",
                    "contact_type": str(contact_type.id)
                }
            ]
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, RegulatingBody.objects.count())
        self.assertEquals(1, Contact.objects.count())

    def test_upate_contact_invalid(self):
        url = reverse("api:facilities:regulating_bodies_list")
        reg_body = mommy.make(RegulatingBody)
        url = url + "{}/".format(reg_body.id)
        contact_type = mommy.make(ContactType)
        data = {

            "contacts": [
                {
                    "contact_type": str(contact_type.id)
                }
            ]
        }
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(1, RegulatingBody.objects.count())
        self.assertEquals(0, Contact.objects.count())
