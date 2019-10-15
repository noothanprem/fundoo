import redis
from django.http import HttpResponse
from .redisfunc import RedisOperations
rds = redis.StrictRedis(host='localhost', port=6379, db=0)


def token_required(view_func):

    def wrap(r,rs,*args, **kwargs):
        robj=RedisOperations()
        rds=robj.r
        header=rs.META['HTTP_AUTHORIZATION']
        print(header)
        headerlist=header.split(" ")
        headertoken=headerlist[1]
        redistoken=rds.get(headertoken)
        print(redistoken)
        if redistoken is not None:
            print("tokenisnotnoneeeeeee")
            return view_func(r,rs,*args, **kwargs)
        else:
            print("logout unsuccesssful")
            return HttpResponse("Logout unsuccessful")
    return wrap
         