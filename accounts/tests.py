import requests
import json

with open("/home/admin81/fundoo/fundooproject/accounts/test.json") as f:
    data=json.load(f)
print(data)


reg =  { "username":"",
         "email":"",
         "password":""
                    }

class Test_Registration:
    
    def test_Registration_validinput(self):
        url="http://127.0.0.1:8000/register"
 
        print(data)
        # user = reg
        Response=requests.post(url,reg)
    
        assert Response.status_code == 200

    def test_Registration_nullinput(self):
        url="http://127.0.0.1:8000/register"
        print("hellooooo",data)
        user=data['register'][1]
        print("haiiiiii",user)
        Response=requests.post(url,user)
        assert Response.status_code == 200


    

if __name__ == "__main__":
    Test_Registration()