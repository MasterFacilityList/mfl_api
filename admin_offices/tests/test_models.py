from django.test import TestCase

from model_mommy import mommy

from ..models import AdminOffice, AdminOfficeContact


class TestAdminOffice(TestCase):
    def test_save(self):
        mommy.make(AdminOffice)
        self.assertEquals(1, AdminOffice.objects.count())


class TestAdminOfficeContact(TestCase):
    def test_save(self):
        mommy.make(AdminOfficeContact)
        self.assertEquals(1, AdminOfficeContact.objects.count())
