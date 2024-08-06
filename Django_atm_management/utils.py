from datetime import datetime, timedelta
from functools import wraps
from urllib import response

import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

# Secret key for signing the JWT
SECRET_KEY = settings.SECRET_KEY

# Token expiration time
ACCESS_TOKEN_LIFETIME = timedelta(minutes=5)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)


def generate_access_token(user):
    expiration = datetime.utcnow() + ACCESS_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    expiration = datetime.utcnow() + REFRESH_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return JsonResponse({"message": "Token is expired"}, status=status.HTTP_498_INVALID_TOKEN)
    except jwt.InvalidTokenError:
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)


def is_auth(fun):
    @wraps(fun)
    def wrap(request, *args, **kwargs):
        print("Line 49>>>", request.headers)
        print("Line 50", request, *args, **kwargs)
        # print("Line 51>>>",request.data)

        try:
            token = request.headers['Authorization']

            if not token:
                return JsonResponse({"message": "Token is missing!"}, status=status.HTTP_403_FORBIDDEN)

            decode_token_result = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # (token)

            request.decoded_token_result = decode_token_result
            request.user_id = request.decoded_token_result.get("user_id")
            return fun(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token is expired"}, status=status.HTTP_498_INVALID_TOKEN)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return JsonResponse({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    return wrap

    # except jwt.InvalidTokenError:
    #  return None
