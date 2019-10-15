import redis



class RedisOperations:
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
       
    def save(self,token):
        self.r.set(token,token)

