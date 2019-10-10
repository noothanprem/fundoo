import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

class RedisOperations:
       
    def save(self,token):
        r.set(token,token)


        
