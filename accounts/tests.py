import requests
import json

with open('test.json') as f:
    data=json.load(f)
print(data)

class Test_Registration:
    
    def test_Registration_validinput(self):
        url="http://127.0.0.1:8000/register/"
 
        print(data)
        user = data['register'][0]
        Response=requests.post(url,user)
        assert Response.status_code == 200

if __name__ == "__main__":
    Test_Registration()