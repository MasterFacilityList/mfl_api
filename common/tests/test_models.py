from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ..models import (
    Contact, Province, County, District,
    Division, Location, SubLocation, Constituency)


class TestContactModel(TestCase):
    def test_save_contact(self):
        contact_data = {
            "email": "test@mail.com",
            "town": "Ughaibuni",
            "postal_code": "00900",
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
            "postal_code": "00900",
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
            "postal_code": "00900",
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
            "postal_code": "00900",
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
        Constituency.objects.create(**constituency_data)
        self.assertEquals(1, Constituency.objects.count())

    def test_unicode(self):
        const = Constituency.objects.create(
            name="jina", code='some code', county=self.county)
        self.assertEquals("jina", const.__unicode__())


class TestDistrictModel(TestCase):
    def test_save_district(self):
        county = County.objects.create(name="county x", code="XCounty")
        data = {
            "name": "some name",
            "code": "code",
            "county": county
        }
        District.objects.create(**data)
        self.assertEquals(1, District.objects.count())

    def test_unicode(self):
        county = County.objects.create(name="county x", code="XCounty")
        data = {
            "name": "some name",
            "code": "code",
            "county": county
        }
        dis = District.objects.create(**data)
        self.assertEquals(dis.__unicode__(), "some name")


class TestDivisionModel(TestCase):
    def test_save_division(self):
        county = County.objects.create(name="countyy", code="asf")
        district = District.objects.create(
            name="Baringo", code="BA", county=county)
        data = {
            "name": "Ichamus",
            "code": "ICHA",
            "district": district
        }
        Division.objects.create(**data)
        self.assertEquals(1, Division.objects.count())

    def test_unicode(self):
        county = County.objects.create(name="countyy", code="asf")
        district = District.objects.create(
            name="Baringo", code="BA", county=county)
        data = {
            "name": "Ichamus",
            "code": "ICHA",
            "district": district
        }
        division = Division.objects.create(**data)
        self.assertEquals("Ichamus", division.__unicode__())


class TestLocationModel(TestCase):
    def test_save_location(self):
        county = County.objects.create(name="countyy", code="asf")
        district = District.objects.create(
            name="Baringo", code="BA", county=county)
        division = Division.objects.create(
            name="Tenwek", code="TEN", district=district)
        location_data = {
            "name": "Mogogosiek",
            "code": "MOG",
            "division": division
        }
        location = Location.objects.create(**location_data)
        self.assertEquals(1, Location.objects.count())

        # test unicode
        self.assertEquals(location_data.get("name"), location.__unicode__())


class TestSublocationModel(TestCase):
    def test_save_sublocation(self):
        province = Province.objects.create(name="Rift Valley", code="RV")
        county = County.objects.create(
            name="county", code="asf")
        district = District.objects.create(
            name="Baringo", code="BA", county=county, province=province)
        constituency = Constituency.objects.create(
            name="Constituency", code="cons", county=county)
        division = Division.objects.create(
            name="Tenwek", code="TEN", district=district,
            constituency=constituency)
        location = Location.objects.create(
            name="Mogogosiek", code="MOG", division=division)
        sub_location_data = {
            "name": "emurwa",
            "code": "EMU",
            "location": location
        }
        sub_location = SubLocation.objects.create(**sub_location_data)
        self.assertEquals(1, SubLocation.objects.count())

        # test location
        self.assertEquals(location, sub_location.location)

        # test get sublocation's division
        self.assertEquals(division, sub_location.division)

        # test get sublocation's district
        self.assertEquals(district, sub_location.district)

        # test get sublocation's county
        self.assertEquals(county, sub_location.county)

        # test get sublocation's province
        self.assertEquals(province, sub_location.province)

        # test get sublocation's constituency
        self.assertEquals(
            constituency, sub_location.constituency)

        # test sublocations _unicode
        self.assertEquals("emurwa", sub_location.__unicode__())
