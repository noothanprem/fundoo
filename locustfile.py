from locust import HttpLocust, TaskSet

def login(l):
    l.client.post("/login", {"username":"nisam", "password":"pressurecooker315"})


class UserBehavior(TaskSet):

    def on_start(self):
        login(self)



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000