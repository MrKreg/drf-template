from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.authtoken.models import Token


def get_user_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


def encode_uid(pk):
    return urlsafe_base64_encode(force_bytes(pk))


def decode_uid(pk):
    return force_text(urlsafe_base64_decode(pk))