from __future__ import unicode_literals

import pdb

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
from .serializer import UploadImageSerializer, NoteShareSerializer, NoteSerializer, LabelSerializer
from .Lib.amazon_s3_file import UploadImage
from .models import Note, Label
from .service.label import LabelOperations
from .Lib.redisfunction import RedisOperation
from django.core.exceptions import ObjectDoesNotExist
redisobject=RedisOperation()
redis=redisobject.r


uploadclassobject = UploadImage()
labelobject = LabelOperations()


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


class CreateLabel(GenericAPIView):
    serializer_class = LabelSerializer

    def get(self, request):
        print (request.user)
        response = labelobject.get_label(request)

        return HttpResponse(json.dumps(response))

    def post(self, request):
        # import pdb
        # pdb.set_trace()
        print (request.user,"user inside create postttttttttt")
        response = labelobject.create_label(request)
        return HttpResponse(json.dumps(response))


class UpdateLabel(GenericAPIView):
    serializer_class = LabelSerializer

    def put(self,request,label_id):

        response = labelobject.update_label(request,label_id)
        return HttpResponse(json.dumps(response))

    def delete(self,request,label_id):

        response = labelobject.delete_label(request, label_id)
        return HttpResponse(json.dumps(response))




class CreateNote(GenericAPIView):

    serializer_class = NoteSerializer


    # method for creating the data
    def post(self, request):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            # pdb.set_trace()
            data=request.data
            print (request.data,"request daaataaaaaaaaaaaaaaaaaaaaaaa")
            user=request.user
            print (data['label'],"Labels beforrrrrrrrrrrreeeeeeeeeeee")
            user_id=user.id
            print (data,"daaaaatttttaaaaaaaaaaaaaaaaaaaaaa")
            print (type(data),"typeofdaaaataaaaaaaaaaaaa")
            collab_list=[]
            label_list=[]
            labels=data['label']
            print (labels,"Labelllllllllllll")
            for label in labels:
                labelobject=Label.objects.filter(user_id=user_id,name=label)
                print (labelobject,"labelobjecttttt")
                label_id=labelobject.values()[0]['id']
                print (label_id,"labelllliddddddd")
                label_list.append(label_id)
            data['label']=label_list
        except TypeError:
            print("Type Errrorrrrrrrrrrr")

        collaborators=data['collab']
        print (collaborators,"colllaaaaboratorrrrr")
        for collaborator in collaborators:
            collaborator_object=User.objects.filter(email=collaborator)
            print (collaborator_object,"colllab objecttttt")
            print (collaborator_object,"colllaaaaboraaatorobjecttt")
            collaborator_id=collaborator_object.values()[0]['id']
            print (collaborator_id,"collaboratoridddddd")
            collab_list.append(collaborator_id)
        data['collab']=collab_list


        serializer=NoteSerializer(data=data,partial=True)
        print (serializer.initial_data)
        if serializer.is_valid():

            create_note=serializer.save(user=user)
            print (create_note.id,"create note iddddddddd")
            redis.set(create_note.id,str(json.dumps(serializer.data)))
            response['success']=True
            response['message']="Data saved successfully"
            response['data']=""
            return HttpResponse(json.dumps(response))



class UpdateNote(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self,request,note_id):
        response = {"success": False,
                    "message": "",
                    "data": ""}
        redis_data=redis.get(str(note_id))
        if redis_data is not None:
            note=Note.objects.filter(id=note_id)
            print (note,"Note objectttttttttt")
            note_contents=note.values()
            note_content=note_contents[0]
            response['success']=True
            response['message']="Read Operation Successful"
            response['data']=note_content
            return HttpResponse(json.dumps(response))







