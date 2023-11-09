from rest_framework.authentication import BaseAuthentication,get_authorization_header
from rest_framework import exceptions
from .models import User
from .token_jwt import decode_access_token
from django.core.cache import caches


class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_heaader = get_authorization_header(request)
        # print(authorization_heaader)
        if not authorization_heaader:
            return None
        try:
            access_token = authorization_heaader
            payload = decode_access_token(access_token)
            if not caches['auth'].keys(payload['jti']):
                raise exceptions.AuthenticationFailed("TOken not valid")    
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        
        user = User.objects.filter(id = payload['acoount_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return (user,payload)


