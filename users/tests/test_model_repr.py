from django.test import TestCase

from common.tests import ModelReprMixin
from users import models


class TestModelRepr(ModelReprMixin, TestCase):

    def test_user(self):
        self.check_repr(
            models.MflUser(first_name="fname", last_name="lname"),
            "fname lname"
        )

    def test_oauth_app(self):
        self.check_repr(
            models.MFLOAuthApplication(name="app"),
            "app"
        )
        self.check_repr(
            models.MFLOAuthApplication(client_id="client id"),
            "client id"
        )
