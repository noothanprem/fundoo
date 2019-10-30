import json
import jwt
from django.conf import settings
from django.contrib.auth.models import User

from django.http import HttpResponse

from .Lib.redisfunction import RedisOperation

redisobject=RedisOperation()
redis=redisobject.r

def login_decorator(function):
    def wrapper(request,*args,**kwargs):
        response = {"success": False,
                    "message": "Invalid User",
                    "data": ""}

        if request.COOKIES.get(settings.SESSION_COOKIE_NAME):
            user = request.COOKIES.get(settings.SESSION_COOKIE_NAME)

            if user:
                return function(request, *args, **kwargs)
            else:
                return HttpResponse(json.dumps(response))

        else:
            http_header = request.META["HTTP_AUTHORIZATION"]
            token = http_header.split(" ")
            decoded_token = jwt.decode(token[1], settings.SECRET_KEY)
            user = User.objects.get(id=decoded_token['user_id'])
            redis.get(user.username)
            return function(request, *args, **kwargs)
    return wrapper
