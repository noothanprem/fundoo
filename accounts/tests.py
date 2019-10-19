import requests
import json

with open("/home/admin81/fundoo/fundooproject/accounts/test.json") as f:
    data=json.load(f)
print(data)



class Test_Registration:
    
    def test_Registration_validinput(self):
        url="http://127.0.0.1:8000/accounts/register"
        user=data['register'][0]
        Response=requests.post(url,user)
    
        assert Response.status_code == 200

    def test_Registration_nullinput(self):
        url="http://127.0.0.1:8000/accounts/register"
        user=data['register'][1]
        Response=requests.post(url,user)
        assert Response.status_code == 404

class Test_Login:
    def test_Login_validinput(self):
        url="http://127.0.0.1:8000/accounts/login"
        user=data['login'][0]
        Response=requests.post(url,user)
        assert Response.status_code == 200

    def test_Login_nullinput(self):
        url="http://127.0.0.1:8000/accounts/login"
        user=data['login'][1]
        Response=requests.post(url,user)
        assert Response.status_code == 404

class Test_ForgotPassword:
    def test_ForgotPassword_validinput(self):
        url="http://127.0.0.1:8000/accounts/forgotpassword"
        user=data['forgotpassword'][0]
        Response=requests.post(url,user)
        assert Response.status_code == 200

    def test_ForgotPassword_nullinput(self):
        url="http://127.0.0.1:8000/accounts/forgotpassword"
        user=data['forgotpassword'][1]
        Response=requests.post(url,user)
        assert Response.status_code == 404





    

if __name__ == "__main__":
    Test_Registration()