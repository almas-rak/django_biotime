from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import logout
from datetime import timedelta
from .models import TokenLife


class TokenFromCookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token_key = request.COOKIES.get('auth_token')
        if not token_key:
            return None

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        try:
            token_lifetime = TokenLife.objects.get(user_pk_id=token.user_id).limit_life
        except TokenLife.DoesNotExist:
            token_lifetime = 240  # Дефолтное значение

        if token.created < timezone.now() - timedelta(minutes=token_lifetime):
            token.delete()
            logout(request)
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)
