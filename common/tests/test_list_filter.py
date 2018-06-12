import pytest

from django.conf import settings
from model_mommy import mommy
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from common.models import County


@pytest.fixture
def user():
    user = mommy.make(
        settings.AUTH_USER_MODEL, email='email@email.com',
        first_name='first_name', last_name='last_name', is_active=True)
    user.set_password('reallyLONG1$')
    return user


@pytest.fixture
def client(user):
    cli = APIClient()
    cli.force_authenticate(user)
    return cli


@pytest.mark.django_db
def test_list_filter(client):
    mommy.make(County, name='a', code=1)
    mommy.make(County, name='b', code=2)
    mommy.make(County, name='c', code=3)

    # strings
    url = reverse('api:common:counties_list') + "?name=a,b"
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data['results']) == 2

    # numbers
    url = reverse('api:common:counties_list') + "?code=1,2"
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data['results']) == 2

    # combined
    url = reverse('api:common:counties_list') + "?code=1&name=a,b"
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data['results']) == 1

    # stupid shit
    url = reverse('api:common:counties_list') + "?code=1,"
    resp = client.get(url)
    assert resp.status_code == 200
    assert len(resp.data['results']) == 1
