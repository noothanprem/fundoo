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

    response = {"success": False,
                "message": "",
                "data": []}
    """
    function to create label
    """
    def create_label(self,request):
        """

        :param request: to create label
        :return: creates label
        """



        try:
            """
            gets the label name
            """
            name = request.data['name']

            """
            gets the user from the request object
            """
            user=request.user
            user_id=request.user


            """
            getting the user with the given id
            """
            userobject=User.objects.get(id=user.id)

            """
            checks whether the label with the same name and user exists or not
            """
            if Label.objects.filter(user_id=user_id,name=name).exists():

                self.response['message'] = "Label already exists."

                return self.response

            """
            creating label
            """
            labelobject=Label.objects.create(name=name, user=userobject)
            self.response['success']=True
            self.response['message']="Label created successfully"
            self.response['data'].append(name)
            logger.info("Label created successfully")
        except Label.DoesNotExist:
            logger.info("Exception occured while accessing the user")

            self.response['message'] = "Exception occured while accessing the user"


        return self.response

    """
    function to get the label
    """
    def get_label(self,request):
        """

        :param request:get the labels of the user
        :return: returns all the labels of that particular user
        """


        try:
            print ("Inside labelllllllllll")
            """
            getting the user
            """
            user = request.user


            """
            getting the labels of the user
            """
            labels = Label.objects.filter(user_id=user.id)

            labels_list = []
            """
            looping through the labels and getting the name of each label
            """
            for label in labels:
                labels_list.append(label.name)


            logger.info("Read Operation Successfull")
            self.response['success']=True
            self.response['message']="Read Operation Successfull"
            self.response['data'].append(labels_list)
        except Label.DoesNotExist:
            logger.info("Exception occured while getting the Label")

            self.response['message']="Exception occured while getting the Label"

        return self.response

    """
    Function to update label
    takes the label_id as a parameter
    """
    def update_label(self,request,label_id):
        """

        :param request:to update the particular label
        :param label_id: id of the label to be updated
        :return: updates the label
        """


        try:
            """
            getting the user
            """
            user=request.user

            """
            getting the request body contents
            """
            request_body=request.body
            body_unicode = request_body.decode('utf-8')
            body_unicode_dict=json.loads(body_unicode)

            """
            getting the label with the given id
            """
            label_object=Label.objects.get(id=label_id,user_id=user.id)
            """
            replacing the label name
            """
            label_object.name=body_unicode_dict['name']

            label_object.save()

            logger.info("Label Updated Successfully")
            self.response['success'] = True
            self.response['message'] = "Label Updated Successfully"


        except Label.DoesNotExist:
            logger.error("Exception occured while getting the Label object")

            self.response['message'] = "Exception occured while getting the Label object"

        except Exception:
            logger.error("Exception occured")

            self.response['message'] = "Exception occured while getting the Label object"


        return self.response

    """
    function for deleting label
    takes label_id as a parameter
    """
    def delete_label(self,request,label_id):
        """

        :param request: to delete the particular label
        :param label_id: id of the label to be deleted
        :return: deletes the given label
        """



        try:
            #pdb.set_trace()
            """
            getting the user
            """
            user = request.user
            user_id = user.id
            """
            getting the label with the given label_id and user
            """
            label_object = Label.objects.get(id=label_id, user_id=user_id)

            """
            deleting the label
            """
            label_object.delete()
            logger.info("Label Deleted Successfully")
            self.response['success'] = True
            self.response['message'] = "Label Deleted Successfully"


        except Label.DoesNotExist:
            logger.error("Exception occured while getting the Label object")

            self.response['message'] = "Exception occured while getting the Label object"


        return self.response



