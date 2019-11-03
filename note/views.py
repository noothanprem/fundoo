from __future__ import unicode_literals

import logging
import pdb

from requests import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from smtplib import SMTPException
from django.utils.safestring import mark_safe
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import boto3

from fundooproject.settings import file_handler
from .serializer import UploadImageSerializer, NoteShareSerializer, NoteSerializer, LabelSerializer
from .Lib.amazon_s3_file import UploadImage
from .models import Note, Label
from .service.label import LabelOperations
from .service.note import NoteOperations
from .Lib.redisfunction import RedisOperation
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.decorators import method_decorator
from .decorators import login_decorator

redisobject=RedisOperation()
redis=redisobject.r


uploadclassobject = UploadImage()
labelobject = LabelOperations()
noteobject=NoteOperations()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

"""
API for uploading image
"""
class UploadImage(GenericAPIView):
    serializer_class = UploadImageSerializer

    def post(self, request):

        """

        :param request: gives the image for upload
        :return: uplads the images into s3 bucket

        """
        try:
            image = request.FILES.get('imgs')
            print(image, "imaaaaaageeeeeeeeeeeeee")

            """
            calls the upload_file() method inside Lib file
            """
            response = uploadclassobject.upload_file(image)
            # returns the responses

            return HttpResponse(json.dumps(response))
        except Exception:
            response = self.smd_response(False, 'Upload unsuccessful', '')
            return HttpResponse(json.dumps(response))


# API for sharing of notes
class NoteShare(GenericAPIView):
    """
    setting the serializer class
    """
    serializer_class = NoteShareSerializer

    def post(self, request):
        """

        :param request: to share the note to social media
        :return: shares to social media
        """
        """
        
        getting the title and note from notesupload.html
        """
        title = request.data['title']
        note = request.data['note']

        """
        prompts the user if any of the field is empty
        """
        if title == "" or note == "":
            response = self.smd_response(False, 'Please fill the fields', '')
            return HttpResponse(json.dumps(response))
        return render(request, 'notesupload.html', {'title': title, 'note': note})

@method_decorator(login_decorator, name='dispatch')
class Trash(GenericAPIView):

    #serializer_class = NoteSerializer
    response = {"success": False,
                "message": "",
                "data": []}

    def get(self,request):

        try:
            user=request.user
            user_id=user.id
            noteobject=Note.objects.filter(user_id=user_id,is_trash=True)
            notevalues_str=str(noteobject.values())
        except Note.DoesNotExist:
            self.response['message']="Exception occured while accessing note"
            return HttpResponse(json.dumps(self.response))
        self.response['success']=True
        self.response['message']="Trash Get operation successful"
        self.response['data'].append(notevalues_str)
        return HttpResponse(json.dumps(self.response))

@method_decorator(login_decorator, name='dispatch')
class Archieve(GenericAPIView):


    def get(self,request):

        try:
            user=request.user
            print (user,"archieve useeeeerrrrr")
            user_id=user.id
            print (user_id)
            noteobject=Note.objects.filter(user_id=user_id, is_archieve=True)
            print (noteobject,"Archieve note objectt")
            print (type(noteobject),"type note objectttttttt")
            string_note=str(noteobject.values())
        except Note.DoesNotExist:
            self.response['message']="Exception occured while accessing note"
            return HttpResponse(json.dumps(self.response))
        return HttpResponse(json.dumps(string_note))

@method_decorator(login_decorator, name='dispatch')
class Reminder(GenericAPIView):

    response = {"success": False,
                "message": "",
                "data": []}

    def get(self,request):

        try:
            user=request.user
            print (user,"userrrrrrr")
            user_id=user.id
            print (user_id,"user iddddd")
            noteobjects=Note.objects.filter(user_id=user_id)
            str_noteobjects=str(noteobjects)
            remaining_list=[]
            completed_list=[]
            for noteobject in noteobjects:

                if getattr(noteobject,'reminder') > timezone.now():
                    remaining_list.append(noteobject.reminder)
                else:
                    completed_list.append(noteobject.reminder)
            reminders={
                "remaining":remaining_list,
                "completed":completed_list
            }
            reminder_string=str(reminders)
            print (remaining_list,"remaining listtttttttttttttttttttttttttt")
            print (completed_list,"completed listtttttttttttttttttttt")
            self.response['success']=True
            self.response['message']="Reminder operation successful"
            self.response['data'].append(reminder_string)

        except Note.DoesNotExist:
            self.response['message']="Exception occured while accessing the note"
            return HttpResponse(json.dumps(self.response))
        return HttpResponse(json.dumps(self.response))





#API for Label operations
@method_decorator(login_decorator, name='dispatch')
class CreateLabel(GenericAPIView):
    serializer_class = LabelSerializer

    """
    gets the required label
    """
    def get(self, request):
        """

        :param request: requests for label
        :return: returns the label data

        """
        print (request.user)
        """
        calling the get_label() method
        """
        response = labelobject.get_label(request)

        return HttpResponse(json.dumps(response))

    """
    creates label
    """
    def post(self, request):
        """

        :param request: requests to create a label
        :return: creates a label and returns the new label data

        """
        # import pdb
        # pdb.set_trace()
        """
        calls the create_label function
        """
        response = labelobject.create_label(request)
        return HttpResponse(json.dumps(response))

"""
API which performs update and delete label
"""
@method_decorator(login_decorator, name='dispatch')
class UpdateLabel(GenericAPIView):
    serializer_class = LabelSerializer

    def put(self,request,label_id):
        """

        :param request: requests to update a particular label
        :param label_id: id of the label to update
        :return: updates the label and returns the new label data

        """

        """
        calls the update_label function
        """

        print ("Inside putttttttt")
        response = labelobject.update_label(request,label_id)
        if response == "":
            return HttpResponse(json.dumps(response),status=404)
        else:
            return HttpResponse(json.dumps(response))

    def delete(self,request,label_id):

        """

        :param request: requests to delete a particular label
        :param label_id: id of the label to delete
        :return: deletes the label

        """

        """
        calls the delete_label function
        """
        response = labelobject.delete_label(request, label_id)
        return HttpResponse(json.dumps(response))


"""
API for creating note
"""

@method_decorator(login_decorator, name='dispatch')
class CreateNote(GenericAPIView):

    serializer_class = NoteSerializer


    def post(self, request):
        """

        :param request: requests to create a note with the given data
        :return: returns the new note data

        """


        """
        calls the create_note() method
        """
        print ("Inside note post method")
        response=noteobject.create_note(request)
        print (response,"After response from create note post")
        if response['success'] == False:
            return HttpResponse(json.dumps(response),status=400)
        else:
            return HttpResponse(json.dumps(response))

"""
API for reading,updating and deleting notes
"""
@method_decorator(login_decorator, name='dispatch')
class UpdateNote(GenericAPIView):

    serializer_class = NoteSerializer

    def get(self,request,note_id):

        """

        :param request: requests for a particular note data
        :param note_id: id of the note
        :return: returns the requested note datas

        """

        """
        calls the get_note() method
        """
        response=noteobject.get_note(request,note_id)
        print (response,"responseee")

        """
        'default=str' converts everything it doesn't know to strings.
        """
        if (response['success'] == False):
            return HttpResponse(json.dumps(response), status=400)
        else:
            return HttpResponse(json.dumps(response))

    def put(self,request,note_id):

        """

        :param request: requests to update a particular note
        :param note_id: id of the note to update
        :return: updates the note and returns the updated data

        """

        """
        calls the update_note() method
        """
        print (request,"requesttttttttttttt")

        response = noteobject.update_note(request, note_id)
        if(response['success'] == False):
            return HttpResponse(json.dumps(response),status=400)
        else:
            return HttpResponse(json.dumps(response))



    def delete(self,request,note_id):

        """

        :param request: requests to delete a particular note
        :param note_id: id of the note to delete
        :return: deletes the note

        """

        """
        calls the delete_note method
        """
        print ("Inside deleteeeeeeeee")
        response = noteobject.delete_note(request, note_id)
        print(response,"responseeeeeeeee")
        if(response['success'] == False):
            print ("Falseeeeeeeeeee")
            return HttpResponse(json.dumps(response),status=400)
        else:
            print ("elseeeeeeeee")
            return HttpResponse(json.dumps(response))



