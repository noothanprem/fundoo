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
from django.utils import timezone
from django.utils.decorators import method_decorator
from .decorators import login_decorator

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



@method_decorator(login_decorator, name='dispatch')
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

        print (data,"creeeaaateeenooteee daaaataaaaaaaa")
        serializer=NoteSerializer(data=data,partial=True)
        print (serializer.initial_data)
        print ("Before valiiiddddddd")
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

    def put(self,request,note_id):
        response = {"success": False,
                    "message": "",
                    "data": ""}

        note_object=Note.objects.get(id=note_id)
        request_data=request.data
        user=request.user
        user_id=request.user.id
        label_list=[]
        collaborator_list=[]
        print (request_data,"request daaataaaaaaaaaaaaaaaa")
        print (user_id,"request_useeeeerrrrrrrrrrrr")
        labels=request_data['label']
        print(labels,"laaaaabeeeeeelsslistttttttt")
        for label in labels:
            label_object=Label.objects.filter(user=user_id, name=label)
            print (label_object,"laaabeeellll objeeeccccttttttt")
            # getting the value of 'id' from the object
            print(label_object.values(),"llaaabeeel object valueeessssss")
            label_id=label_object.values()[0]['id']
            label_list.append(label_id)
        request_data['label']=label_list


        collaborators=request_data['collab']
        for collaborator in collaborators:
            print (collaborator,"collllaaaaborattooorrr")
            collaborator_object=User.objects.get(email=collaborator)
            print (collaborator_object,"collaaaaaboratorrr objeccccttttt")
            collaborator_id=collaborator_object.id
            print (collaborator_id,"Collaborator_idddddddddddddddddddddddddddddddddddddddd")
            collaborator_list.append(collaborator_id)
        request_data['collab']=collaborator_list
        print (request_data,"requeesssttt daaaataaaaaaaaaaa")
        serializer=NoteSerializer(note_object,data=request_data,partial=True)
        print (serializer,"serializzzzzeeerrrrrrrr")
        if serializer.is_valid():

            update_note=serializer.save()
            print (update_note,"note updaaaateeeeeedddddd")
            response['success'] = True
            response['message'] = "Update Operation Successful"
            response['data'] = request_data
            return HttpResponse(json.dumps(response))


    def delete(self,request,note_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            note=Note.objects.get(id=note_id)
            note.is_delete=True
            note.save()

            response['success'] = True
            response['message'] = "Delete Operation Successful"
            response['data'] = note_id
        except Exception:
            response['success'] =False
            response['message'] = "Delete Operation Failed"
            response['data'] = note_id

        return HttpResponse(json.dumps(response))



class Trash(GenericAPIView):

    serializer_class = NoteSerializer
    def get(self,request):

        response = {"success": False,
                    "message": "",
                    "data": ""}
        user_id=request.user.id
        print (user_id,"ussserrrrr iddddd")
        note=Note.objects.filter(user_id=user_id,is_delete=True)
        print (note)

        return HttpResponse(note.values())


class Archieve(GenericAPIView):
    serializer_class = NoteSerializer

    def get(self,request):
        response = {"success": False,
                    "message": "",
                    "data": ""}

        user_id=request.user.id
        note=Note.objects.filter(user_id=user_id,is_archieve=True)
        return HttpResponse(note.values())




class Reminder(GenericAPIView):

    serializer_class = NoteSerializer
    def get(self,request):

        response = {"success": False,
                    "message": "",
                    "previous_list": "",
                    "pending_list":""
                    }

        user=request.user
        pending_list=[]
        previous_list=[]
        reminder_list = Note.objects.all().values()
        print (reminder_list,"remindrrrrlissstttttttt")
        print (reminder_list.values()[0]['reminder'],"remindeeerrr valuessss")
        for i in range(len(reminder_list)):
             if(timezone.now() >= reminder_list.values()[i]['reminder']):
                 previous_list.append(reminder_list.values()[i]['title'])
             else:
                 pending_list.append(reminder_list.values()[i]['title'])


        response['success']=True
        response['message']="Reminder Get Operation successful"
        response['previous_list']=previous_list
        response['pending_list']=pending_list

        return HttpResponse(json.dumps(response))