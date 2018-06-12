from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from users.models import MflUser
from facilities.models import (
    Facility, FacilityApproval, FacilityStatus
)
from facilities.tests.test_facility_views import load_dump
from facilities.serializers import FacilitySerializer

from common.models import (
    UserSubCounty, SubCounty, Ward, UserCounty, UserConstituency,
    County, Constituency)
from common.tests.test_views import default, LoginMixin


class TestFacilityFilterApprovedAndPublished(APITestCase):

    def setUp(self):
        self.url = reverse("api:facilities:facilities_list")
        self.view_unpublished_perm = Permission.objects.get(
            codename="view_unpublished_facilities")
        self.view_approved_perm = Permission.objects.get(
            codename="view_unapproved_facilities")
        self.view_classified_perm = Permission.objects.get(
            codename="view_classified_facilities")
        self.view_closed_perm = Permission.objects.get(
            codename="view_closed_facilities")
        self.view_rejected_perm = Permission.objects.get(
            codename="view_rejected_facilities")
        self.public_group = mommy.make(Group, name="public")
        view_fields_perm = Permission.objects.get(
            codename='view_all_facility_fields')
        self.admin_group = mommy.make(Group, name="mfl admins")
        self.admin_group.permissions.add(self.view_unpublished_perm.id)
        self.admin_group.permissions.add(self.view_approved_perm.id)
        self.admin_group.permissions.add(self.view_classified_perm.id)
        self.admin_group.permissions.add(view_fields_perm.id)
        self.admin_group.permissions.add(self.view_closed_perm.id)
        self.admin_group.permissions.add(self.view_rejected_perm.id)

        self.admin_user = mommy.make(MflUser, first_name='admin')
        self.public_user = mommy.make(MflUser, first_name='public')

        self.public_user.groups.add(self.public_group)
        self.admin_user.groups.add(self.admin_group)

        self.assertTrue(self.admin_user.has_perm(
            "facilities.view_unpublished_facilities"))
        self.assertTrue(self.admin_user.has_perm(
            "facilities.view_unapproved_facilities"))
        self.assertTrue(self.admin_user.has_perm(
            "facilities.view_classified_facilities"))

        super(TestFacilityFilterApprovedAndPublished, self).setUp()

    def test_public_cant_see_unpublished_facilities(self):
        mommy.make(Facility)
        op_status = mommy.make(FacilityStatus, is_public_visible=True)
        mommy.make(Facility, rejected=True)
        facility_2 = mommy.make(
            Facility, operation_status=op_status)
        mommy.make(FacilityApproval, facility=facility_2)
        self.assertTrue(facility_2.approved)
        facility_2.is_published = True
        facility_2.save()

        # test admin user sees all facilities
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(3, admin_response.data.get("count"))

        # test public user sees only published facilities
        self.client.logout()
        self.client.force_authenticate(self.public_user)
        public_response = self.client.get(self.url)
        self.assertEquals(200, public_response.status_code)
        self.assertEquals(1, public_response.data.get("count"))
        for obj in public_response.data.get("results"):
            self.assertTrue(
                Facility.objects.get(id=obj.get('id')).is_published)
            self.assertFalse(
                Facility.objects.get(id=obj.get('id')).rejected)

    def test_public_cant_see_unapproved_facilities(self):
        mommy.make(Facility)
        op_status = mommy.make(FacilityStatus, is_public_visible=True)
        facility_2 = mommy.make(
            Facility, approved=True, operation_status=op_status)
        mommy.make(FacilityApproval, facility=facility_2)
        facility_2.is_published = True
        facility_2.save()

        # test admin user sees all facilities
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(2, admin_response.data.get("count"))

        # test public user sees only approved facilities
        self.client.logout()
        self.client.force_authenticate(self.public_user)
        public_response = self.client.get(self.url)
        self.assertEquals(200, public_response.status_code)
        self.assertEquals(1, public_response.data.get("count"))
        for obj in public_response.data.get("results"):
            self.assertTrue(
                Facility.objects.get(id=obj.get('id')).approved)

    def test_public_cant_see_classified_facilities(self):
        mommy.make(Facility, is_classified=True)
        op_status = mommy.make(FacilityStatus, is_public_visible=True)
        facility_2 = mommy.make(Facility, operation_status=op_status)
        mommy.make(FacilityApproval, facility=facility_2)
        facility_2.is_published = True
        facility_2.save()

        # test admin user sees all facilities
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(2, admin_response.data.get("count"))

        # test public user sees only non classified facilities
        self.client.logout()
        self.client.force_authenticate(self.public_user)
        public_response = self.client.get(self.url)
        self.assertEquals(200, public_response.status_code)
        self.assertEquals(1, public_response.data.get("count"))
        for obj in public_response.data.get("results"):
            self.assertFalse(
                Facility.objects.get(id=obj.get('id')).is_classified)

    def test_admin_user_sees_all_fields_list_endpoint(self):
        perm = Permission.objects.get(codename="view_all_facility_fields")
        self.admin_group.permissions.add(perm.id)
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.url)
        all_data = load_dump(response.data['results'], default=default)
        data = all_data[0]
        self.assertIn('has_edits', data)
        self.assertIn('is_approved', data)
        self.assertIn('latest_update', data)
        self.assertIn('deleted', data)
        self.assertIn('active', data)
        self.assertIn('is_classified', data)
        self.assertIn('is_published', data)
        self.assertIn('created_by', data)
        self.assertIn('updated_by', data)

    def confirm_data_detail_endpoint_contains_keys(self, data):
        self.assertIn('has_edits', data)
        self.assertIn('is_approved', data)
        self.assertIn('latest_update', data)
        self.assertIn('deleted', data)
        self.assertIn('active', data)
        self.assertIn('search', data)
        self.assertIn('is_classified', data)
        self.assertIn('is_published', data)
        self.assertIn('approved', data)
        self.assertIn('regulated', data)
        self.assertIn('rejected', data)
        self.assertIn('created_by', data)
        self.assertIn('updated_by', data)

    def test_admin_user_sees_all_fields_on_detail(self):
        perm = Permission.objects.get(codename="view_all_facility_fields")
        self.admin_group.permissions.add(perm.id)
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        self.client.logout
        self.client.force_authenticate(self.admin_user)
        url = self.url + "{}/".format(facility.id)
        response = self.client.get(url)
        data = load_dump(response.data, default=default)
        self.confirm_data_detail_endpoint_contains_keys(data)

    def test_get_empy_list(self):
        # test admin user sees all facilities
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(0, admin_response.data.get("count"))

    def test_admin_user_sees_closed_facilities(self):
        mommy.make(Facility, closed=True)
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(1, admin_response.data.get("count"))

    def test_public_does_not_see_closed_facilities(self):
        mommy.make(Facility, closed=True)
        self.client.force_authenticate(self.public_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(0, admin_response.data.get("count"))

    def test_admin_user_sees_rejected_facilities(self):
        mommy.make(Facility, rejected=True)
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(1, admin_response.data.get("count"))

    def test_public_does_not_see_rejected_facilities(self):
        mommy.make(Facility, rejected=True)
        self.client.force_authenticate(self.public_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(0, admin_response.data.get("count"))

    def test_sub_county_users_facilities(self):
        # test that sub-county users see facilities only in their sub-county
        user = mommy.make(MflUser, is_superuser=True)
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        sub = mommy.make(SubCounty, county=county)
        mommy.make(UserSubCounty, user=user, sub_county=sub)
        ward = mommy.make(Ward, sub_county=sub, constituency=const)
        mommy.make(Facility, ward=ward)
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self.client.logout()

    def test_sub_county_and_consituency_facilities(self):
        # Test users assigned to constituencies and sub-counties
        # at the same time only see the facilities in the sub-county
        user_1 = mommy.make(MflUser, is_superuser=True)
        county = mommy.make(County)
        mommy.make(UserCounty, county=county, user=user_1)
        user = mommy.make(MflUser, is_superuser=True)
        sub = mommy.make(SubCounty, county=county)
        const = mommy.make(Constituency, county=county)
        mommy.make(
            UserConstituency, user=user, constituency=const,
            created_by=user_1, updated_by=user_1)
        mommy.make(UserSubCounty, user=user, sub_county=sub)
        ward = mommy.make(Ward, sub_county=sub, constituency=const)
        ward_2 = mommy.make(Ward, constituency=const)
        mommy.make(Facility, ward=ward)
        mommy.make(Facility, ward=ward_2)
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))


class TestFacilitiesPendingApprovalFilter(LoginMixin, APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:facilities_list")
        super(TestFacilitiesPendingApprovalFilter, self).setUp()

    def test_get_facilities_pending_approval(self):
        self.maxDiff = None
        facility = mommy.make(Facility)
        facility_2 = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility_2)
        facility_3 = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility_3)
        facility_3.name = 'new name'
        facility_3.save()

        url = self.url + "?pending_approval=true"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get("count"))

        expected_results = [
            FacilitySerializer(facility).data,
            FacilitySerializer(facility_3).data]
        self.assertListEqual(
            sorted(load_dump(expected_results, default=default)),
            sorted(load_dump(response.data.get("results"), default=default)))

        url = self.url + "?pending_approval=false"
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        expected_results = [
            FacilitySerializer(facility_2).data
        ]
        self.assertListEqual(expected_results, response.data.get("results"))
