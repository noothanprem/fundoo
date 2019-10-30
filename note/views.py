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

# API for uploading image
class UploadImage(GenericAPIView):
    serializer_class = UploadImageSerializer

    def post(self, request):
        try:
            image = request.FILES.get('imgs')
            print(image, "imaaaaaageeeeeeeeeeeeee")

            # calls the upload_file() method inside Lib file
            response = uploadclassobject.upload_file(image)
            # returns the responses

            return HttpResponse(json.dumps(response))
        except Exception:
            response = self.smd_response(False, 'Upload unsuccessful', '')
            return HttpResponse(json.dumps(response))


# API for sharing of notes
class NoteShare(GenericAPIView):
    # setting the serializer class
    serializer_class = NoteShareSerializer

    def post(self, request):
        # getting the title and note from notesupload.html
        title = request.data['title']
        note = request.data['note']

        # prompts the user if any of the field is empty
        if title == "" or note == "":
            response = self.smd_response(False, 'Please fill the fields', '')
            return HttpResponse(json.dumps(response))
        return render(request, 'notesupload.html', {'title': title, 'note': note})


#API for Label operations
@method_decorator(login_decorator, name='dispatch')
class CreateLabel(GenericAPIView):
    serializer_class = LabelSerializer

    #gets the required label
    def get(self, request):
        print (request.user)
        #calling the get_label() method
        response = labelobject.get_label(request)

        return HttpResponse(json.dumps(response))

    #creates label
    def post(self, request):
        # import pdb
        # pdb.set_trace()
        #calls the create_label function
        response = labelobject.create_label(request)
        return HttpResponse(json.dumps(response))

#API which performs update and delete label
@method_decorator(login_decorator, name='dispatch')
class UpdateLabel(GenericAPIView):
    serializer_class = LabelSerializer

    def put(self,request,label_id):
        #calls the update_label function
        response = labelobject.update_label(request,label_id)
        return HttpResponse(json.dumps(response))

    def delete(self,request,label_id):
        #calls the delete_label function
        response = labelobject.delete_label(request, label_id)
        return HttpResponse(json.dumps(response))


#API for creating note
@method_decorator(login_decorator, name='dispatch')
class CreateNote(GenericAPIView):

    serializer_class = NoteSerializer


    def post(self, request):

        #calls the create_note() method
        response=noteobject.create_note(request)
        return HttpResponse(json.dumps(response))

#API for reading,updating and deleting notes
@method_decorator(login_decorator, name='dispatch')
class UpdateNote(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self,request,note_id):
        #calls the get_note() method
        response=noteobject.get_note(request,note_id)

        #'default=str' converts everything it doesn't know to strings.
        return HttpResponse(json.dumps(response,default=str))

    def put(self,request,note_id):
        #calls the update_note() method
        response = noteobject.update_note(request, note_id)
        return HttpResponse(json.dumps(response))



    def delete(self,request,note_id):
        #calls the delete_note method
        response = noteobject.delete_note(request, note_id)
        return HttpResponse(json.dumps(response))


