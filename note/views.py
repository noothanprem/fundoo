from __future__ import unicode_literals
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
from .serializer import UploadImageSerializer, NoteShareSerializer,NoteSerializer,LabelSerializer
from .Lib.amazon_s3_file import UploadImage
from .models import Note,Label
from .service.label import LabelOperations
from django.core.exceptions import ObjectDoesNotExist

uploadclassobject=UploadImage()
labelobject=LabelOperations()

# API for uploading image
class UploadImage(GenericAPIView):
    serializer_class = UploadImageSerializer

    def post(self, request):
        try:
            image = request.FILES.get('imgs')
            print(image,"imaaaaaageeeeeeeeeeeeee")


            #calls the upload_file() method inside Lib file
            response = uploadclassobject.upload_file(image)
            #returns the responses

            return  HttpResponse(json.dumps(response))
        except Exception:
            response = self.smd_response(False, 'Upload unsuccessful', '')
            return HttpResponse(json.dumps(response))



#API for sharing of notes
class NoteShare(GenericAPIView):
    #setting the serializer class
    serializer_class = NoteShareSerializer

    def post(self, request):
        # getting the title and note from notesupload.html
        title = request.data['title']
        note = request.data['note']

        # prompts the user if any of the field is empty
        if (title == "" or note == ""):
            response = self.smd_response(False, 'Please fill the fields', '')
            return HttpResponse(json.dumps(response))
        return render(request, 'notesupload.html', {'title': title, 'note': note})


class LabelView(GenericAPIView):
    serializer_class =LabelSerializer

    def post(self, request):

        # import pdb
        # pdb.set_trace()
        response=labelobject.create_label(request)
        return HttpResponse(json.dumps(response))

class Note(GenericAPIView):
    serializer_class = NoteSerializer



    #method for creating the data
    def post(self,request):


        try:

            #requestData=json.dumps(request.data)
            #print(requestData)
            title = request.data["title"]
            note = request.data["note"]
            user=request.data["user"]
            label=request.data["label"]
            collaborators=request.data["collab"]
            is_archieve=request.data["is_archieve"]
            print(is_archieve)
            pin=request.data["pin"]
            url=request.data["url"]
            try:
                image=request.data['image']
            except Exception:
                return HttpResponse("Image file exception")

        except KeyError:
            return HttpResponse("keyerror")

        # uploadresponse = uploadclassobject.upload_file(image)
        # print (uploadresponse)
        userobject=User.objects.get(id=user)
        print (userobject,"userobjecttttttttttt")
        noteobject=Note(title=title,note=note,user=userobject,is_archieve=is_archieve,pin=pin,url=url)
        print (noteobject,"noteobjecttttttttt")
        noteobject.save()
        noteobject.label.add(label)
        noteobject.collab.add(collaborators)

        # print('title : ',title,)
        # print ('note : ',note)
        # print ('user : ',user)
        # print('label : ',label)
        # print ('collaborators : ',collaborators)
        # print ('image : ',image)
        # print ('is_archieve : ',is_archieve)
        # print ('pin : ',pin)
        # print ('url : ',url)
        # return HttpResponse("success")


