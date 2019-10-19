import redis
from django.http import HttpResponse
from .redisfunc import RedisOperations
rds = redis.StrictRedis(host='localhost', port=6379, db=0)

#decorator to check whether the token is valid or not
def token_required(view_func):

    def wrap(r,rs,*args, **kwargs):
        #creating the object of RedisOperations()
        redisobject=RedisOperations()
        redisdata=redisobject.r

        #getting the request header
        try:
            header=rs.META['HTTP_AUTHORIZATION']
        except Exception:
            print ("Exception occured while accessing the request header")
        print(header)
        #splitting the header to make a list
        headerlist=header.split(" ")

        #getting the token from the list
        headertoken=headerlist[1]
        #trying to access the token from redis using the token got from request header
        redistoken=rds.get(headertoken)
        print(redistoken)

        #If we got the token in redis, then the token is valid. so, move forward
        if redistoken is not None:
            return view_func(r,rs,*args, **kwargs)
        else:
            print("logout unsuccesssful")
            return HttpResponse("Logout unsuccessful")
    return wrap
         