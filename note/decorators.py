import json
import pdb

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
        print ("inside decoratorrrrrrrrrrrr")
        if request.COOKIES.get(settings.SESSION_COOKIE_NAME):
            user = request.COOKIES.get(settings.SESSION_COOKIE_NAME)

            if user:
                print ("Helloooooooooo")
                return function(request, *args, **kwargs)
            else:
                return HttpResponse(json.dumps(response))

        else:

            http_header = request.META["HTTP_AUTHORIZATION"]
            print (http_header,"htttp headerrrrr")
            token = http_header.split(" ")
            print (token,"tokennnnnn")
            decoded_token = jwt.decode(token[1], settings.SECRET_KEY)
            print (decoded_token,"decoded tokennnnnnn")
            user = User.objects.get(id=decoded_token['user_id'])
            redis.get(user.username)
            return function(request, *args, **kwargs)
    return wrapper
