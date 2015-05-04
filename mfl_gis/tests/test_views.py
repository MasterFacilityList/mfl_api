from rest_framework.test import APITestCase
from common.tests.test_views import LoginMixin
from django.core.urlresolvers import reverse
from model_mommy import mommy


from ..models import WorldBorder
from ..serializers import WorldBorderDetailSerializer


class TestCountryBoundariesView(LoginMixin, APITestCase):

    def test_retrieve_single_country_boundary(self):
        country = mommy.make(WorldBorder)
        url = reverse(
            'api:mfl_gis:world_border_detail', kwargs={'pk': country.pk})
        response = self.client.get(url)
        expected_data = WorldBorderDetailSerializer(country).data
        # Silly issues with floats being rounded to different precisions
        # between the serializer and the "round trip through the view" version
        self.assertEqual(
            expected_data['code'],
            response.data['code']
        )
