import redis
from django.http import HttpResponse
from .Lib.redisfunc import RedisOperations
rds = redis.StrictRedis(host='localhost', port=6379, db=0)

#decorator to check whether the token is valid or not
def token_required(view_func):

    def wrap(r,request,*args, **kwargs):
        #creating the object of RedisOperations()
        redisobject=RedisOperations()
        redisdata=redisobject.r

        #getting the request header
        try:
            header=request.META['HTTP_AUTHORIZATION']
        except Exception:
            print ("Exception occured while accessing the request header")

        #splitting the header to make a list
        headerlist=header.split(" ")

        #getting the token from the list
        headertoken=headerlist[1]

        #trying to access the token from redis using the token got from request header
        redistoken=redisdata.get(headertoken)


        #If we got the token in redis, then the token is valid. so, move forward
        if redistoken is not None:
            return view_func(r,request,*args, **kwargs)
        else:
            print("logout unsuccesssful")
            return HttpResponse("Logout unsuccessful")
    return wrap
         