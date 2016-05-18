from django.utils.translation import ugettext_lazy
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from captcha.models import CaptchaStore, get_safe_now


class CaptchaField(serializers.Serializer):
    hashkey = serializers.CharField(required=False, allow_null=True)
    response = serializers.CharField(write_only=True, required=False, allow_null=True)

    default_error_messages = {
        'invalid_captcha': ugettext_lazy('Invalid CAPTCHA')
    }

    def validate(self, attrs):
        response = (attrs.get('response') or '').lower()
        hashkey = attrs.get('hashkey', '')
        CaptchaStore.remove_expired()
        if not self.required and not response:
            pass
        else:
            try:
                CaptchaStore.objects.get(response=response, hashkey=hashkey, expiration__gt=get_safe_now()).delete()
            except CaptchaStore.DoesNotExist:
                raise ValidationError(self.error_messages['invalid_captcha'])
        return {}
