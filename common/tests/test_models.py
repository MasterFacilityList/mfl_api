from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ..models import (
    Contact, Province, County, Location, District,
     Division, Location, SubLocation, Constituency
    )


class TestContactModel(TestCase):
    def test_save_contact(self):
        contact_data = {
            "email": "test@mail.com",
            "town": "Ughaibuni",
            "postal_code":"00900",
            "address": "189",
            "nearest_town": "Uyoma",
            "landline": "020-83573295",
            "mobile": "0756832902",
        }
        Contact.objects.create(**contact_data)
        self.assertEquals(1, Contact.objects.count())
  
    def test_contact_phone_number_validation(self):
        contact_data = {
            "email": "test@mail.com",
            "town": "Ughaibuni",
            "postal_code":"00900",
            "address": "189",
            "nearest_town": "Uyoma",
            "landline": "020-83573295",
            "mobile": "0756832902142",
        }
        with self.assertRaises(ValidationError) as error:
            Contact.objects.create(**contact_data)
            self.assertEquals(
                "The mobile number format is wrong. Use 07XXABCDEF",
                error.message)

    def test_unicode(self):
        contact_data = {
            "email": "test@mail.com",
            "town": "Ughaibuni",
            "postal_code":"00900",
            "address": "189",
            "nearest_town": "Uyoma",
            "landline": "020-83573295",
            "mobile": "0756832902",
        }
        obj = Contact.objects.create(**contact_data)
        self.assertEquals("test@mail.com", obj.__unicode__())

    def test_contact_mobile_not_less_than_ten_charaters(self):
        contact_data = {
            "email": "test@mail.com",
            "town": "Ughaibuni",
            "postal_code":"00900",
            "address": "189",
            "nearest_town": "Uyoma",
            "landline": "020-83573295",
            "mobile": "07568",
        }
        with self.assertRaises(ValidationError) as error:
            Contact.objects.create(**contact_data)
            self.assertEquals(
                "The mobile number format is wrong. Use 07XXABCDEF",
                error.message)


class TestProvinceModel(TestCase):
    def test_save_province(self):
        data = {
            "name": "NYANZA",
            "code": "NYA1"
        }
        Province.objects.create(**data)
        self.assertEquals(1, Province.objects.count())

    def test_unicode(self):
        data = {
            "name": "NYANZA",
            "code": "NYA1"
        }
        Province.objects.create(**data)

    def test_unique_name(self):
        data = {
            "name": "NYANZA",
            "code": "NYA1"
        }
        # create the province with the name NYANZA once
        Province.objects.create(**data)
        # try creating a province with the name again
        with self.assertRaises(IntegrityError):
            p = Province(**data)
            p.save()  


class TestCountyModel(TestCase):

    def test_save_county(self):
        county_data = {
            "name": "WAJIR",
            "code": "WA1"
        }
        County.objects.create(**county_data)
        self.assertEquals(1, County.objects.count())

    def test_unicode(self):
        county_name = "Texas"
        county = County.objects.create(
            name=county_name, code='some code')
        self.assertEquals(county_name, county.__unicode__())


class TestConstituencyModel(TestCase):
    def setUp(self):
        self.county = County.objects.create(
            name='county', code='county code')

    def test_save_constituency(self):
        constituency_data = {
            "name": "KAPSA",
            "code": "1125",
            "county": self.county

        }
        const =  Constituency.objects.create(**constituency_data)
        self.assertEquals(1, Constituency.objects.count())

    def test_unicode(self):
        const = Constituency.objects.create(
            name="jina", code='some code', county=self.county)
        self.assertEquals("jina",const.__unicode__())
