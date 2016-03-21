from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, Permission

from model_mommy import mommy

from common.tests import ViewTestBase
from facilities.models import Facility, FacilityApproval
from users.models import MflUser
from common.models import (
    County, Constituency, UserCounty, UserConstituency, Ward,
    Contact, ContactType,
    UserSubCounty, SubCounty)

from ..models import (
    Status,
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    CHUService,
    CommunityHealthUnitContact
)
from ..serializers import (
    CommunityHealthUnitSerializer,
    CommunityHealthWorkerSerializer,
    CommunityHealthWorkerContactSerializer
)


class TestCHUService(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:chu_services_list")
        super(TestCHUService, self).setUp()

    def test_post(self):
        data = {
            "name": "Kajina tu ka service",
            "description": "Explain kidogo service inaentail nini"
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, CHUService.objects.count())

    def test_get_list(self):
        mommy.make(CHUService, _quantity=5)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(5, response.data.get('count'))

    def test_get_single(self):
        service = mommy.make(CHUService)
        url = self.url + "{}/".format(service.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_patch(self):
        service = mommy.make(CHUService)
        url = self.url + "{}/".format(service.id)
        data = {
            "name": "Jina mpya"
        }
        response = self.client.patch(url, data)
        self.assertEquals(200, response.status_code)
        service_refetched = CHUService.objects.get(id=service.id)
        self.assertEquals(service_refetched.name, data.get('name'))


class TestCommunityHealthUnitView(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:community_health_units_list")
        super(TestCommunityHealthUnitView, self).setUp()

    def test_post_chu(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        data = {
            "facility": facility.id,
            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
        }
        response = self.client.post(self.url, data)
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, CommunityHealthUnit.objects.count())

    def test_post_chu_inlined_chew_and_contacts(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact": "0756477578",
                "contact_type": str(contact_type.id)
            }
        ]
        data = {
            "facility": facility.id,
            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
            "contacts": contacts,
            "health_unit_workers": [
                {
                    "first_name": "Muuguzi",
                    "last_name": "Mnoma",
                    "is_incharge": True
                }
            ]
        }
        response = self.client.post(self.url, data)

        self.assertEquals(201, response.status_code)
        self.assertEquals(1, CommunityHealthUnit.objects.count())
        self.assertEquals(1, Contact.objects.count())
        self.assertEquals(1, CommunityHealthUnitContact.objects.count())

    def test_patch_with_already_added_contacts(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        contact_type = mommy.make(ContactType)
        chu = mommy.make(
            CommunityHealthUnit, facility=facility, status=status)
        con = mommy.make(
            Contact, contact="07246578256", contact_type=contact_type)
        mommy.make(CommunityHealthUnitContact, contact=con, health_unit=chu)
        contacts = [
            {
                "contact": "07246578256",
                "contact_type": str(contact_type.id),
                "id": str(con.id),
            }
        ]

        data = {

            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
            "contacts": contacts
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Contact.objects.count())
        self.assertEquals(1, CommunityHealthUnitContact.objects.count())

    def test_patch_with_already_added_contacts_no_id(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        contact_type = mommy.make(ContactType)
        chu = mommy.make(
            CommunityHealthUnit, facility=facility, status=status)
        con = mommy.make(
            Contact, contact="07246578256", contact_type=contact_type)
        mommy.make(CommunityHealthUnitContact, contact=con, health_unit=chu)
        contacts = [
            {
                "contact": "07246578256",
                "contact_type": str(contact_type.id)
            }
        ]

        data = {

            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
            "contacts": contacts
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Contact.objects.count())
        self.assertEquals(1, CommunityHealthUnitContact.objects.count())

    def test_patch_chu_erroneous_contacts(self):
        chu = mommy.make(CommunityHealthUnit)
        contacts = [
            {
                "not_contact": "23857289",
                "not_contact_type": "q935728572389"
            }
        ]
        data = {
            "contacts": contacts
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)

    def test_patch_chu_inlined_chew(self):
        chu = mommy.make(CommunityHealthUnit)
        chew = mommy.make(CommunityHealthWorker, health_unit=chu)
        data = {
            "households_monitored": 100,
            "health_unit_workers": [
                {
                    "id": str(chew.id),
                    "first_name": "Muuguzi tabibu",
                    "last_name": "Mnoma",
                    "is_incharge": True
                }
            ]
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, CommunityHealthUnit.objects.count())
        self.assertEquals(
            CommunityHealthWorker.objects.all()[0].first_name,
            "Muuguzi tabibu")

    def test_post_chu_inlined_chew_invalid_data(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        data = {
            "facility": facility.id,
            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
            "health_unit_workers": [
                {
                    "is_incharge": True
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)

    def test_post_inlined_invalid_contacts(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact": "07246578256",
                "contact_type": str(contact_type.id)
            }
        ]
        contact_type.delete()
        data = {
            "facility": facility.id,
            "name": "test community",
            "status": status.id,
            "households_monitored": 100,
            "contacts": contacts
        }
        response = self.client.post(self.url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, Contact.objects.count())
        self.assertEquals(0, CommunityHealthUnitContact.objects.count())

    def test_update_chu_inlined_invalid_contacts(self):
        facility = mommy.make(Facility)
        status = mommy.make(Status)
        chu = mommy.make(
            CommunityHealthUnit, facility=facility, status=status)
        contact_type = mommy.make(ContactType)
        contacts = [
            {
                "contact": "07246578256",
                "contact_type": str(contact_type.id)
            }
        ]
        contact_type.delete()
        data = {
            "name": "test community",
            "households_monitored": 100,
            "contacts": contacts
        }
        url = self.url + "{}/".format(chu.id)
        response = self.client.patch(url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(0, Contact.objects.count())
        self.assertEquals(0, CommunityHealthUnitContact.objects.count())

    def test_list_community_health_units(self):
        group = mommy.make(Group)
        published_facilities_perm = Permission.objects.get(
            codename='view_unpublished_facilities')
        rejected_chu_perm = Permission.objects.get(
            codename='view_rejected_chus')
        group.permissions.add(published_facilities_perm)
        group.permissions.add(rejected_chu_perm)
        self.user.groups.add(group)
        self.user.is_national = True
        self.user.save()
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()
        health_unit = mommy.make(CommunityHealthUnit, facility=facility)
        health_unit_2 = mommy.make(CommunityHealthUnit, facility=facility)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                CommunityHealthUnitSerializer(
                    health_unit_2,
                    context={
                        'request': response.request
                    }
                ).data,
                CommunityHealthUnitSerializer(
                    health_unit,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(
            expected_data['results'], response.data['results']
        )

    def test_retrieve_single_health_unit(self):
        health_unit = mommy.make(CommunityHealthUnit)
        url = self.url + "{}/".format(health_unit.id)
        response = self.client.get(url)
        expected_data = CommunityHealthUnitSerializer(
            health_unit,
            context={
                'request': response.request
            }
        ).data

        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)

    def test_filter_chus_pending_approval(self):
        self.user.is_superuser = True
        self.user.save()
        mommy.make(CommunityHealthUnit, is_approved=True)
        mommy.make(CommunityHealthUnit, has_edits=True)
        mommy.make(CommunityHealthUnit, is_rejected=True)
        mommy.make(CommunityHealthUnit)
        url = self.url + "{}".format("?pending_approval=true")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

        url = self.url + "{}".format("?pending_approval=false")
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))

    def test_pdf_details(self):
        health_unit = mommy.make(CommunityHealthUnit)
        url = reverse(
            "api:chul:chu_detail_report", kwargs={"pk": health_unit.pk}
        )
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, "chu_details.html")

    def test_filter_chus_by_sub_county(self):
        county_user = mommy.make(MflUser, is_superuser=True)
        county = mommy.make(County)
        const = mommy.make(Constituency, county=county)
        mommy.make(UserCounty, user=county_user, county=county)

        sub_county_user = mommy.make(MflUser, is_superuser=True)
        sub_county = mommy.make(SubCounty, county=county)
        ward = mommy.make(Ward, constituency=const, sub_county=sub_county)
        mommy.make(UserSubCounty, user=sub_county_user, sub_county=sub_county)
        facility = mommy.make(Facility, ward=ward)
        mommy.make(CommunityHealthUnit, facility=facility)
        url = reverse("api:chul:community_health_units_list")
        self.client.force_authenticate(sub_county_user)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))


class TestCommunityHealthWorkerView(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:community_health_workers_list")
        super(TestCommunityHealthWorkerView, self).setUp()

    def test_health_workers_listing(self):
        worker_1 = mommy.make(CommunityHealthWorker)
        worker_2 = mommy.make(CommunityHealthWorker)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                CommunityHealthWorkerSerializer(
                    worker_2,
                    context={
                        'request': response.request
                    }
                ).data,
                CommunityHealthWorkerSerializer(
                    worker_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self.maxDiff = None
        self._assert_response_data_equality(
            expected_data['results'], response.data['results']
        )

    def test_retrieve_single_worker(self):
        worker = mommy.make(CommunityHealthWorker)
        expected_data = CommunityHealthWorkerSerializer(
            worker, context={
                'request': {
                    "REQUEST_METHOD": "None"
                }
            }
        ).data
        url = self.url + "{}/".format(worker.id)
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)


class TestCommunityHealthWokerContactView(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:community_health_worker_contacts_list")
        super(TestCommunityHealthWokerContactView, self).setUp()

    def test_health_workers_contact_list(self):
        contact_1 = mommy.make(CommunityHealthWorkerContact)
        contact_2 = mommy.make(CommunityHealthWorkerContact)
        response = self.client.get(self.url)
        expected_data = {
            "results": [
                CommunityHealthWorkerContactSerializer(
                    contact_2,
                    context={
                        'request': response.request
                    }
                ).data,
                CommunityHealthWorkerContactSerializer(
                    contact_1,
                    context={
                        'request': response.request
                    }
                ).data
            ]
        }
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(
            expected_data['results'], response.data['results']
        )

    def test_retrieve_single_health_worker_contact(self):
        contact = mommy.make(CommunityHealthWorkerContact)
        url = self.url + "{}/".format(contact.id)
        response = self.client.get(url)
        expected_data = CommunityHealthWorkerContactSerializer(
            contact,
            context={
                'request': response.request
            }
        ).data
        self.assertEquals(200, response.status_code)
        self._assert_response_data_equality(expected_data, response.data)


class TestCommunityUnitsFiltering(ViewTestBase):

    def setUp(self):
        self.url = reverse("api:chul:community_health_units_list")
        self.test_group = mommy.make(Group)
        self.rejected_chu_perm = Permission.objects.get(
            codename="view_rejected_chus")
        self.test_group.permissions.add(self.rejected_chu_perm)
        self.published_facilities_perm = Permission.objects.get(
            codename='view_unpublished_facilities')
        self.test_group.permissions.add(self.published_facilities_perm)
        super(TestCommunityUnitsFiltering, self).setUp()

    def test_national_admin_sees_all_chus(self):
        user = mommy.make(MflUser, is_national=True)
        user.groups.add(self.test_group)

        ward_1 = mommy.make(Ward)
        ward_2 = mommy.make(Ward)
        facility_1 = mommy.make(Facility, ward=ward_1)
        facility_2 = mommy.make(Facility, ward=ward_2)
        chu_1 = mommy.make(CommunityHealthUnit, facility=facility_1)
        chu_2 = mommy.make(CommunityHealthUnit, facility=facility_2)
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(2, response.data.get('count'))
        self._assert_response_data_equality(
            [
                CommunityHealthUnitSerializer(chu_2).data,
                CommunityHealthUnitSerializer(chu_1).data
            ],
            response.data.get('results'))

    def test_schrio_sees_only_chus_in_jurisdiction(self):
        user = mommy.make(MflUser)
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        constituency_2 = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)
        ward_2 = mommy.make(Ward, constituency=constituency_2)

        mommy.make(UserCounty, user=user, county=county)
        user_2 = mommy.make(MflUser)
        user_2.groups.add(self.test_group)
        mommy.make(
            UserConstituency,
            constituency=constituency, user=user_2,
            created_by=user, updated_by=user)
        self.client.force_authenticate(user_2)
        facility_1 = mommy.make(Facility, ward=ward)
        facility_2 = mommy.make(Facility, ward=ward_2)
        chu = mommy.make(CommunityHealthUnit, facility=facility_1)
        mommy.make(CommunityHealthUnit, facility=facility_2)

        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

        self.assertEquals(1, response.data.get('count'))
        self._assert_response_data_equality(
            [
                CommunityHealthUnitSerializer(chu).data
            ],
            response.data.get('results'))

    def test_chrio_see_only_chus_in_jurisdiction(self):
        user = mommy.make(MflUser)
        user.groups.add(self.test_group)
        county = mommy.make(County)
        constituency = mommy.make(Constituency, county=county)
        ward = mommy.make(Ward, constituency=constituency)

        mommy.make(UserCounty, user=user, county=county)
        self.client.force_authenticate(user)
        facility_1 = mommy.make(Facility, ward=ward)
        facility_2 = mommy.make(Facility)
        chu = mommy.make(CommunityHealthUnit, facility=facility_1)
        mommy.make(CommunityHealthUnit, facility=facility_2)

        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))
        self._assert_response_data_equality(
            [
                CommunityHealthUnitSerializer(chu).data
            ],
            response.data.get('results'))

    def _publish_facility(self, facility):
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()

    def test_public_user_sees_all_chus(self):
        public_user = mommy.make(MflUser)
        facility = mommy.make(Facility)
        self._publish_facility(facility)
        chu = mommy.make(
            CommunityHealthUnit, facility=facility, is_approved=True)
        mommy.make(
            CommunityHealthUnit, facility=facility, is_rejected=True)
        self.client.force_authenticate(public_user)
        self.client.force_authenticate(public_user)
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.data.get('count'))

        self._assert_response_data_equality(
            [CommunityHealthUnitSerializer(chu).data],
            response.data.get('results'))
