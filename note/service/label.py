import pdb

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from note.models import Label
import json
import logging
from fundoo_notes.settings import file_handler
from note.lib.redisfunction import RedisOperation

redisobject = RedisOperation()
redis = redisobject.r


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
            user_id=user.id


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
            labelobject = Label.objects.create(name=name, user=userobject)

            string_userid=str(user_id)
            redis.hmset(string_userid + "label", {labelobject.id: name})
            logger.info("note is created")
            """
            creating label
            """

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

        global label_name
        try:
            print ("Inside labelllllllllll")
            """
            getting the user
            """
            user = request.user


            """
            getting the labels of the user
            """
            user = request.user
            string_userid=str(user.id)
            userlabels = redis.hvals(string_userid + "label")
            userlabelsstring=str(userlabels)
            print(userlabels,"from redisssss")

            if userlabels is None:
                print("redis data is none")
                labels = Label.objects.filter(user_id=user.id)
                userlabelsstring = [i.name for i in labels]
                logger.info("labels where fetched from database for user :%s", request.user)

            logger.info("labels where fetched from redis")

            self.response['success']=True
            self.response['message']="Read Operation Successfull"
            self.response['data'].append(userlabelsstring)
        except Label.DoesNotExist:
            logger.info("Exception occured while getting the Label")

            self.response['message']="Exception occured while getting the Label"

        return self.response




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
            string_user_id=str(user.id)
            redis.hmset(string_user_id + "label", {label_object.id: label_id})

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
            string_user_id=str(user_id)
            redis.hdel(string_user_id + "label", label_id)
            logger.info("Label Deleted Successfully")
            self.response['success'] = True
            self.response['message'] = "Label Deleted Successfully"


        except Label.DoesNotExist:
            logger.error("Exception occured while getting the Label object")

            self.response['message'] = "Exception occured while getting the Label object"


        return self.response



