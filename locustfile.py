from locust import HttpLocust, TaskSet


def login(l):
    l.client.post("/login", {"username": "nisam", "password": "admin@123"})



def index(l):
    l.client.get("/")


def profile(l):
    l.client.get("/home")


class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        profile(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
