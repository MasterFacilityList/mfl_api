from django.test import TestCase
from model_mommy import mommy

from common import models
from common.tests import ModelReprMixin


class TestModelRepr(ModelReprMixin, TestCase):

    def test_abstract(self):
        with self.assertRaises(NotImplementedError):
            models.AbstractBase().__str__()

        with self.assertRaises(NotImplementedError):
            models.AbstractBase().__unicode__()

    def test_contact_type(self):
        x = "twirra"
        self.check_repr(models.ContactType.objects.create(name=x), x)

    def test_contact(self):
        ct = models.ContactType.objects.create(name="twirra")
        self.check_repr(
            models.Contact.objects.create(contact_type=ct, contact="@w"),
            "twirra: @w"
        )

    def test_county(self):
        x = "nai"
        self.check_repr(models.County.objects.create(name=x), x)

    def test_constituency(self):
        x = "mathare"
        c = models.County.objects.create(name="k")
        self.check_repr(
            models.Constituency.objects.create(name=x, county=c), x
        )

    def test_ward(self):
        x = "nai"
        c = models.County.objects.create(name="k")
        con = models.Constituency.objects.create(name="con", county=c)
        self.check_repr(
            models.Ward.objects.create(name=x, constituency=con), x
        )

    def test_sub_county(self):
        x = "mahali"
        c = models.County.objects.create(name="k")
        self.check_repr(models.SubCounty.objects.create(name=x, county=c), x)

    def test_user_contact(self):
        ct = models.ContactType.objects.create(name="twirra")
        contact = models.Contact.objects.create(contact="@m", contact_type=ct)
        user = mommy.make(
            models.settings.AUTH_USER_MODEL, first_name="fname",
            last_name="lname"
        )
        self.check_repr(
            models.UserContact.objects.create(user=user, contact=contact),
            "fname lname: (twirra: @m)"
        )

    def test_user_county(self):
        county = models.County.objects.create(name="county")
        user = mommy.make(
            models.settings.AUTH_USER_MODEL, first_name="fname",
            last_name="lname"
        )
        self.check_repr(
            models.UserCounty.objects.create(user=user, county=county),
            "fname lname: county"
        )

    def test_user_constituency(self):
        c = models.County.objects.create(name="k")
        cons = models.Constituency.objects.create(name="cons", county=c)
        user = mommy.make(
            models.settings.AUTH_USER_MODEL, first_name="fname",
            last_name="lname"
        )
        self.check_repr(
            models.UserConstituency(user=user, constituency=cons),
            "fname lname: cons"
        )

    def test_town(self):
        x = "tao"
        self.check_repr(models.Town.objects.create(name=x), x)

    def test_physical_address(self):
        x = "ile place"
        self.check_repr(
            models.PhysicalAddress.objects.create(location_desc=x), x
        )

    def test_document_upload(self):
        x = "implementation guide"
        self.check_repr(models.DocumentUpload(name=x,), x)

    def test_user_sub_county(self):
        c = models.County.objects.create(name="k")
        sub = models.SubCounty.objects.create(name="sub", county=c)
        user = mommy.make(
            models.settings.AUTH_USER_MODEL, first_name="fname",
            last_name="lname", email='a@b.com'
        )
        self.check_repr(
            models.UserSubCounty(user=user, sub_county=sub),
            "a@b.com - sub"
        )
