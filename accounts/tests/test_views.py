import requests
import json
class Test_Registration:
    
    def test_Registration_validinput(self):
        url="http://127.0.0.1:8000/register"
        data=json.load('test.json')
        print(data)
        user = data['register'][0]
        Response=requests.post(url,user)
        assert Response.status_code == 200
