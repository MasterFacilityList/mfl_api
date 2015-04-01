from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import (
    Contact,
    )


class TestModels(TestCase):
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






