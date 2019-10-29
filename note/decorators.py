import json

from django.http import HttpResponse
from fundooproject import settings

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

