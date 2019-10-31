from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from note.models import Note,Label
from note.Lib.redisfunction import RedisOperation
from note.serializer import NoteSerializer
from fundooproject.settings import file_handler
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

redisobject=RedisOperation()
redis=redisobject.r

class NoteOperations:

    #Function for creating note
    def create_note(self,request):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            # pdb.set_trace()
            #getting the data from request
            data = request.data
            print (data,"request daaaataaaaaaaaa")
            #getting the user
            user = request.user
            user_id = user.id
            print (user,"userrrrrrrrrrr")
            #creating the lists for collaborators and labels
            collab_list = []
            label_list = []
            labels = data['label']
            print (labels,"labelllllllllssssssssss")
            #iterates through all the labels in the list
            for label in labels:
                #getting each label and adding the label_id to the list
                labelobject = Label.objects.filter(user_id=user_id, name=label)
                print (labelobject,"labelobjecttttttt")
                if not labelobject:
                    raise Label.DoesNotExist
                label_id = labelobject.values()[0]['id']
                print (label_id,"labell idddddddd")
                label_list.append(label_id)
            #replaces the 'label' in data with the new label_list
            data['label'] = label_list
        except Label.DoesNotExist:
            response['success']=False
            response['message']="Exception occured while accessing the label"
            response['data']=""
            return response
        except KeyError:
            logger.error("Key Error")
            pass
            #response['success'] = False
            #response['message'] = "Key Error occured1"
            #response['data'] = ""
            #return response

        #getting the given collaborators

        try:
            collaborators = data['collab']
            #Iterates through all the collaborators
            for collaborator in collaborators:
                #getting the collaborators with the given email
                collaborator_object = User.objects.filter(email=collaborator)
                print (collaborator_object,"collaboratorobjectt")
                if not collaborator_object:
                    raise User.DoesNotExist
                #getting the id of the collaborator
                collaborator_id = collaborator_object.values()[0]['id']
                print (collaborator_id, "collaboratoridddddd")
                #adding all the ids to the list
                collab_list.append(collaborator_id)

            #replaces in the data with the new list
            data['collab'] = collab_list
            print (data,"data after collaaaabbb")
        except KeyError:
            logger.error("Key Error")
            pass
            #response['success'] = False
            #response['message'] = "Key Error occured2"
            #response['data'] = ""
            #return response
        except User.DoesNotExist:
            response['success']=False
            response['message']="Exception occured while accessing the User"
            response['data']=""
            return response

        print("Before serializeeerrrrrr")
        #gives 'partial=True' because we are not using all the fileds in the model
        serializer = NoteSerializer(data=data, partial=True)
        print (serializer,"After serializerrrrr")
        if serializer.is_valid():
            #saving
            create_note = serializer.save(user=user)


            #saving to redis with the key as note_id
            redis.set(create_note.id, str(json.dumps(serializer.data)))
            logger.info("note created successfully")
            response['success'] = True
            response['message'] = "Note created successfully"
            response['data'] = ""
            return response
        logger.error("note creation failed")
        response['success'] = False
        response['message'] = "Note creation failed"
        response['data'] = ""
        return response

    #Function to get the note
    #takes note_id as parameter
    def get_note(self,request,note_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}
        try:
            #getting note from redis with the given id
            redis_data = redis.get(str(note_id)).decode('utf-8')
            #getting the data from the database if redis reading fails
            if redis_data is None:
                note = Note.objects.filter(id=note_id)
                note_contents = note.values()
                print(note_contents,"note contentsssssss")
                note_content = note_contents[0]
                logger.info("Data accessed from database")
                return note_content
        except Note.DoesNotExist:
            logger.error("Exception occured while accessing Note")
            response['success'] = False
            response['message'] = "Exception occured while accessing Note"
            response['data'] = ""
            return response
        except KeyError:
            logger.error("Key error occured")
            response['success'] = False
            response['message'] = "Key error occured"
            response['data'] = ""
            return response
        except Exception as e:
            logger.error(str(e))
            response['success'] = False
            response['message'] = str(e)
            response['data'] = ""
            return response

        logger.info("Data accessed from redis")
        response['success'] = True
        response['message'] = "Read Operation Successful"
        response['data'] = redis_data
        return response

    #Function to update the note
    #gets note_id as parameter
    def update_note(self,request,note_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}
        try:
            try:
                #getting the note with the given id
                note_object = Note.objects.get(id=note_id)
                #getting the data from request
                request_data = request.data
                #getting the user
                user = request.user
                user_id = request.user.id
            except Note.DoesNotExist:
                logger.error("Exception occured while accessing Note")
                response['success'] = False
                response['message'] = "Exception occured while accessing Note"
                response['data'] = ""
                return response

            label_list = []
            collaborator_list = []
            try:
                #getting the labels from the request data
                labels = request_data['label']
                #Iterates through the labels
                for label in labels:
                    #getting the label with the given id and name
                    label_object = Label.objects.filter(user=user_id, name=label)

                    if not label_object:
                        raise Label.DoesNotExist
                    # getting the value of 'id'
                    label_id = label_object.values()[0]['id']
                    #adding each labels id to a list
                    label_list.append(label_id)
                #replacing the label data with id's list
                request_data['label'] = label_list
            except Label.DoesNotExist:
                logger.error("Exception occured while accessing Label")
                response['success'] = False
                response['message'] = "Exception occured while accessing Label"
                response['data'] = ""
                return response
            except KeyError:
                logger.error("Key error occured")
                response['success'] = False
                response['message'] = "Key error occured"
                response['data'] = ""
                return response

            ##getting the given collaborators
            collaborators = request_data['collab']
            try:
                #Iterates through the collaborators
                for collaborator in collaborators:
                    #getting the collaborator with the given email
                    collaborator_object = User.objects.filter(email=collaborator)
                    if not collaborator_object:
                        raise User.DoesNotExist
                    # getting the id of the collaborator
                    collaborator_id = collaborator_object.values()[0]['id']

                    # adding all the ids to the list
                    collaborator_list.append(collaborator_id)
                #replacing with the id's list
                request_data['collab'] = collaborator_list

            except User.DoesNotExist:
                logger.error("Exception occured while accessing User")
                response['success'] = False
                response['message'] = "Exception occured while accessing User"
                response['data'] = ""
                return response

            #makes 'partial' as 'True' because we are not using all the fileds of the Note
            serializer = NoteSerializer(note_object, data=request_data, partial=True)
            print (serializer.initial_data,"serializer initial daataaaa")
            print (type(serializer.initial_data),"serializer initial data type")

            if serializer.is_valid():
                print ("valid serializeeeeeeeerrrrrrr")
                #saving
                update_note = serializer.save()

                redis.set(update_note.id, str(json.dumps(serializer.data)))
                logger.info("Update Operation Successful")
                response['success'] = True
                response['message'] = "Update Operation Successful"
                response['data'] = request_data
                return response
        except Exception:
            return HttpResponse(json.dumps(response),status=404)

    #Function to delete the note
    def delete_note(self,request,note_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}
        user=request.user
        try:
            #getting the note with the given id
            note = Note.objects.get(id=note_id,user_id=user.id)
            print (note,"noooottttttttttteeeeeee")
            #making 'is_delete' to access it from Trash
            note.is_delete = True
            note.save()


            logger.info("Delete Operation Successful")
            response['success'] = True
            response['message'] = "Delete Operation Successful"
            response['data'] = note_id

        except Note.DoesNotExist:
            logger.error("Delete Operation Failed")
            response['success'] = False
            response['message'] = "Delete Operation Failed"
            response['data'] = note_id

        except Exception as e:
            logger.error("Delete Operation Failed")
            response['success'] = False
            response['message'] = str(e)
            response['data'] = ""
        return response




