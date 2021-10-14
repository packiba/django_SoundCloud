import datetime
from typing import Optional

import jwt
from django.conf import settings
from rest_framework import authentication, exeptions

from ..models import AuthUser


class AuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request, token=None, **kwargs) -> Optional[tuple]:
        auth_header = authentication.get_authenticatin_header(request).split()

        if not auth_header or auth_header[0].lower() != b'token':
            return None

        if len(auth_header) == 1:
            raise exeptions.AuthenticationFailed('Invalid token header. No credential provided.')
        elif len(auth_header) > 2:
            raise exeptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exeptions.AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credential(token)

    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise exeptions.AuthenticationFailed('Invalid token header. Could not decode token.')

        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise exeptions.AuthenticationFailed('Token expired.')

        try:
            user = AuthUser.objects.get(id=payload['user_id'])
        except AuthUser.DoesNotExist:
            raise exeptions.AuthenticationFailed('No user matching this token was found.')

        return user, None