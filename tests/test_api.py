import json

from django.core.urlresolvers import reverse
from rest_framework import status
from captcha.models import CaptchaStore
import pytest


pytestmark = [pytest.mark.django_db]


def test_captcha_view(client):
    response = client.get(reverse('api-captcha'))
    assert response.status_code == status.HTTP_200_OK
    assert CaptchaStore.objects.filter(hashkey=response.data['hashkey']).exists()


def test_valid_captcha(client):
    response = client.get(reverse('api-captcha'))
    captcha_store = CaptchaStore.objects.get(hashkey=response.data['hashkey'])
    data = {
        'captcha': {
            'hashkey': response.data['hashkey'],
            'response': captcha_store.response
        }
    }
    response = client.post(
        reverse('api-test') + '?required', json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK


def test_empty_captcha(client):
    response = client.get(reverse('api-captcha'))
    data = {
        'captcha': None
    }
    response = client.post(
        reverse('api-test') + '?required', json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['captcha'] == ["This field may not be null."]


def test_invalid_captcha(client):
    response = client.get(reverse('api-captcha'))
    data = {
        'captcha': {
            'hashkey': response.data['hashkey'],
            'response': '1111'
        }
    }
    response = client.post(
        reverse('api-test') + '?required', json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['captcha']['non_field_errors'] == ["Invalid CAPTCHA"]


def test_not_required_captcha(client):
    response = client.get(reverse('api-captcha'))
    data = {
        'captcha': {
            'hashkey': response.data['hashkey'],
            'response': None
        }
    }
    response = client.post(
        reverse('api-test'), json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK


def test_invalid_hashkey(client):
    data = {
        'captcha': {
            'hashkey': '1111',
            'response': None
        }
    }
    response = client.post(
        reverse('api-test') + '?required', json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['captcha']['non_field_errors'] == ["Invalid CAPTCHA"]


def test_audio_url(client):
    from captcha.conf import settings
    settings.CAPTCHA_FLITE_PATH = '/usr/bin/flite'
    response = client.get(reverse('api-captcha'))
    assert response.data['audio_url'] is not None
