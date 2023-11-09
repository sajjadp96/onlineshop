import jwt
import datetime
from rest_framework import exceptions
from config import settings


def create_access_token(id,jti):
    return jwt.encode(
        {
            "acoount_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=settings.EXP_ACCESS_HOUR),
            "iat": datetime.datetime.utcnow(),
            "jti": jti
        },
        settings.SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY, algorithms=settings.TOKEN_ALGORITHM)

        return payload
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Expired token")
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")


def create_refresh_token(id,jti):
    return jwt.encode(
        {
            "acoount_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=settings.EXP_REFRESH_DAY),
            "iat": datetime.datetime.utcnow(),
            "jti": jti
        },
        settings.SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY, algorithms=settings.TOKEN_ALGORITHM)

        return payload["acoount_id"]
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Expired token")
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")
    
    

