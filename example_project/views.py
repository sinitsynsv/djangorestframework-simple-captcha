from rest_framework import serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from rest_framework_captcha.fields import CaptchaField


class RequiredSerializer(serializers.Serializer):
    captcha = CaptchaField()


class NotRequiredSerializer(serializers.Serializer):
    captcha = CaptchaField(required=False)


class TestView(generics.GenericAPIView):

    def get_serializer_class(self):
        if 'required' in self.request.query_params:
            return RequiredSerializer
        else:
            return NotRequiredSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
