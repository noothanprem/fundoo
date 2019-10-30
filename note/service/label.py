import pdb

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from note.models import Label
import json
import logging
from fundooproject.settings import file_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

class LabelOperations:

    #function to create label
    def create_label(self,request):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            #gets the label name
            name = request.data['name']

            #gets the user from the request object
            user=request.user
            user_id=request.user


            #getting the user with the given id
            userobject=User.objects.get(id=user.id)

            #checks whether the label with the same name and user exists or not
            if Label.objects.filter(user_id=user_id,name=name).exists():
                response['success'] = False
                response['message'] = "Label already exists."
                response['data'] = ""
                return response

            #creating label
            labelobject=Label.objects.create(name=name, user=userobject)
            response['success']=True
            response['message']="Label created successfully"
            response['data']=name
            logger.info("Label created successfully")
        except Label.DoesNotExist:
            logger.info("Exception occured while accessing the user")
            response['success'] = False
            response['message'] = "Exception occured while accessing the user"
            response['data'] = ""

        return response

    #function to get the label
    def get_label(self,request):

        response = {"success": False,
                    "message": "",
                    "data": ""}
        try:
            #getting the user
            user = request.user


            #getting the labels of the user
            labels = Label.objects.filter(user_id=user.id)

            labels_list = []
            #looping through the labels and getting the name of each label
            for label in labels:
                labels_list.append(label.name)

            response=labels_list
            logger.info("Read Operation Successfull")
        except Label.DoesNotExist:
            logger.info("Exception occured while getting the Label")
            response['success']=False
            response['message']="Exception occured while getting the Label"
            response['data']=""
        return response

    #Function to update label
    #takes the label_id as a parameter
    def update_label(self,request,label_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            #getting the user
            user=request.user

            #getting the request body contents
            request_body=request.body
            body_unicode = request_body.decode('utf-8')
            body_unicode_dict=json.loads(body_unicode)

            #getting the label with the given id
            label_object=Label.objects.get(id=label_id,user_id=user.id)
            #replacing the label name
            label_object.name=body_unicode_dict['name']

            label_object.save()

            logger.info("Label Updated Successfully")
            response['success'] = True
            response['message'] = "Label Updated Successfully"
            response['data'] = ""

        except Label.DoesNotExist:
            logger.info("Exception occured while getting the Label object")
            response['success'] = False
            response['message'] = "Exception occured while getting the Label object"
            response['data'] = ""

        return response

    #function for deleting label
    #takes label_id as a parameter
    def delete_label(self,request,label_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            #pdb.set_trace()
            #getting the user
            user = request.user
            user_id = user.id
            #getting the label with the given label_id and user
            label_object = Label.objects.get(id=label_id, user_id=user_id)

            #deleting the label
            label_object.delete()
            logger.info("Label Deleted Successfully")
            response['success'] = True
            response['message'] = "Label Deleted Successfully"
            response['data'] = ""

        except Label.DoesNotExist:
            logger.error("Exception occured while getting the Label object")
            response['success'] = False
            response['message'] = "Exception occured while getting the Label object"
            response['data'] = ""

        return response



