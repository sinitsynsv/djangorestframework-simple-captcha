from django.core.urlresolvers import reverse
from rest_framework import decorators
from rest_framework import response
from captcha.models import CaptchaStore
from captcha.conf import settings


@decorators.api_view(['GET'])
def captcha(request):
    key = CaptchaStore.generate_key()
    data = {
        'hashkey': key,
        'image_url': reverse('captcha-image', kwargs={'key': key}),
        'image2x_url': reverse('captcha-image-2x', kwargs={'key': key}),
        'audio_url': None
    }
    if settings.CAPTCHA_FLITE_PATH:
        data['audio_url'] = reverse('captcha-audio', kwargs={'key': key})
    return response.Response(data)
