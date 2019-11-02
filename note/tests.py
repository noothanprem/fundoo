
from django.test import TestCase
import requests
import json
from fundooproject.settings import BASE_URL,TEST_TOKEN
#for testing note functions
with open("test.json") as f:
    data=json.load(f)

headers = {
    'Content_Type': "application/json",
    'Authorization': TEST_TOKEN
}


class TestNote:

     def test_note_post1(self):
         url=BASE_URL+(data[0]['urls']['createnote'])
         input=data[0]['notepost1']
         response=requests.post(url=url,data=input,headers=headers)
         assert response.status_code == 200

     def test_note_post2(self):
         url = BASE_URL+(data[0]['urls']['createnote'])
         input = data[0]['notepost2']
         response = requests.post(url=url, data=input, headers=headers)
         assert response.status_code == 200

     def test_note_post3(self):
         url = BASE_URL+(data[0]['urls']['createnote'])
         input = data[0]['notepost3']
         response = requests.post(url=url, data=input, headers=headers)
         assert response.status_code == 200

     def test_note_post4(self):
         url = BASE_URL+(data[0]['urls']['createnote'])
         input = data[0]['notepost4']
         response = requests.post(url=url, data=input, headers=headers)
         assert response.status_code == 400
     #
     # def test_note_get1(self):
     #    url = BASE_URL + (data[0]['urls']['updatenote'])+"/"+(data[0]['noteget1']['note_id'])
     #    response = requests.get(url=url, headers=headers)
     #    assert response.status_code == 400
     #
     # def test_note_get2(self):
     #    url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+(data[0]['noteget2']['note_id'])
     #    response = requests.get(url=url, headers=headers)
     #    assert response.status_code == 400
     #
     # def test_note_get3(self):
     #     url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+(data[0]['noteget3']['note_id'])
     #     response = requests.get(url=url, headers=headers)
     #     assert response.status_code == 200

     # def test_note_delete1(self):
     #    url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+(data[0]['notedelete1']['note_id'])
     #    response = requests.delete(url=url, headers=headers)
     #    assert response.status_code == 400
     #
     # def test_note_delete2(self):
     #     url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+str((data[0]['notedelete2']['note_id']))
     #     response = requests.delete(url=url, headers=headers)
     #     assert response.status_code == 404
     #
     # def test_note_delete3(self):
     #     url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+(data[0]['notedelete3']['note_id'])
     #     response = requests.delete(url=url, headers=headers)
     #     assert response.status_code == 200

     # def test_note_put1(self):
     #     url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+(data[0]['noteput1']['note_id'])
     #     input = data[0]['notepost1']
     #     response = requests.delete(url=url, data=input, headers=headers)
     #     assert response.status_code == 400
     #
     # def test_note_put2(self):
     #     url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+(data[0]['noteput2']['note_id'])
     #     input=data[0]['notepost1']
     #     response = requests.delete(url=url, data=input,headers=headers)
     #     assert response.status_code == 404
     #
     # def test_note_put3(self):
     #     url = BASE_URL + (data[0]['urls']['updatenote']) + "/"+(data[0]['noteput3']['note_id'])
     #     input = data[0]['notepost1']
     #     response = requests.delete(url=url, data=input, headers=headers)
     #     assert response.status_code == 200


# class TestLabel:
#
#     def test_label_get1(self):
#         url = BASE_URL + (data[0]['urls']['createlabel'])
#         response = requests.get(url=url, headers=headers)
#         assert response.status_code == 200
#
#     def test_label_get2(self):
#         url = BASE_URL + (data[0]['urls']['createlabel'])
#         input=data[0]['labelget2']['label_id']
#         response = requests.get(url=url, data=input, headers=headers)
#         assert response.status_code == 200
#
#     def test_label_put1(self):
#         url = BASE_URL + (data[0]['urls']['updatelabel'])+"/"+(data[0]['labelget2']['label_id'])
#         input=data[0]['labelput2']
#         response = requests.put(url=url, data=input,headers=headers)
#         assert response.status_code == 200
