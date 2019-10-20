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
from .serializer import UploadImageSerializer, NoteShareSerializer
from .Lib.amazon_s3_file import upload_file

# Create your views here.
class UploadImage(GenericAPIView):
    serializer_class = UploadImageSerializer

    def post(self, request):
        try:
            image = request.FILES.get('imgs')
            print(image,"imaaaaaageeeeeeeeeeeeee")
            #s3 = boto3.resource('s3')
            #s3.meta.client.upload_fileobj(image, "hat123", "abc")
            #uploadfileobject=UploadFile()
            #print (uploadfileobject,"uploaaaaaaaaadddddddddddddddddddd")
            response = upload_file(image)
            if response == "success":
                return  HttpResponse("success")
        except Exception:
            return HttpResponse("Upload unsuccessful", status=404)



class NoteShare(GenericAPIView):
    serializer_class = NoteShareSerializer

    def post(self, request):
        title = request.data['title']
        note = request.data['note']
        if(title == "" or note == ""):
            return HttpResponse("Please Fill the fields")
        return render(request, 'notesupload.html', {'title': title, 'note': note})
