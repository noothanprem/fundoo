import requests
from django.conf import settings


class GenerateToken:

    def login_token(self, payload):
        # try:
        response = requests.post(settings.Token, payload)
        return response.json()['access']
        # except Exception:
        # return False