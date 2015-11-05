from django.test import TestCase
from model_mommy import mommy

from chul import models
from common.tests import ModelReprMixin


class TestModelRepr(ModelReprMixin, TestCase):

    def test_status(self):
        x = "hey ya"
        self.check_repr(models.Status.objects.create(name=x), x)

    def test_chuservice(self):
        x = 'jina'
        self.check_repr(mommy.make(models.CHUService, name=x), x)

    def test_chu(self):
        x = "si-hech-yu"
        instance = mommy.make(models.CommunityHealthUnit, name=x, )
        self.check_repr(instance, x)

    def test_chu_contact(self):
        ct = models.Contact._meta.get_field(
            "contact_type").related_model.objects.create(name="twirra")
        contact = models.Contact.objects.create(contact="@m", contact_type=ct)
        chu = mommy.make(models.CommunityHealthUnit, name="c-h-u")
        chu_contact = models.CommunityHealthUnitContact.objects.create(
            health_unit=chu, contact=contact
        )
        self.check_repr(chu_contact, "c-h-u: (twirra: @m)")

    def test_chw(self):
        health_unit = mommy.make(models.CommunityHealthUnit, name='jina')
        instance = mommy.make(
            models.CommunityHealthWorker, first_name="fname",
            health_unit=health_unit
        )
        self.check_repr(instance, "fname (jina)")

    def test_chw_contact(self):
        ct = models.Contact._meta.get_field(
            "contact_type").related_model.objects.create(name="twirra")
        contact = models.Contact.objects.create(contact="@m", contact_type=ct)
        health_unit = mommy.make(models.CommunityHealthUnit, name='jina')

        chw = mommy.make(
            models.CommunityHealthWorker, first_name="fname",
            health_unit=health_unit
        )
        chw_contact = models.CommunityHealthWorkerContact.objects.create(
            health_worker=chw, contact=contact
        )
        self.check_repr(chw_contact, "fname (jina): (twirra: @m)")

    def test_chu_rating(self):
        chu = mommy.make(models.CommunityHealthUnit, name='di chu')
        self.check_repr(models.CHURating(chu=chu, rating=4), 'di chu - 4')
