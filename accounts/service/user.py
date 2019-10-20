from __future__ import unicode_literals
from accounts.serializers import UserSerializer,LoginSerializer, ForgotPasswordSerializer,ResetPasswordSerializer,LogoutSerializer
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
from django.contrib.auth.decorators import login_required
from django_short_url.views import get_surl
import templates
import os

def register_user(request):

    print (request.data["username"])
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']

    message={
        "success":"",
        "message":"",
        "data":""
    }
    print ("After smd formattttttttttttttttttttttttttttttttttttttt")
    # checking whether the user name or email exists or not
    if ((User.objects.filter(username=username).exists()) or (User.objects.filter(email=email).exists())):

        return "Username or email is already taken"
    # checking whether any field is empty or not
    elif username == "" or password == '' or email == '':

        return HttpResponse(json.dumps({"message": "Username or email is empty"}), status=404)
    else:
        print ("Inside the else bodyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        try:

            # Inserting a new row into the database
            user = User.objects.create_user(username=username, email=email, password=password)
            print (user,"In the create userrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        except ObjectDoesNotExist as e:
            print(e)

        user.save()
        user.is_active = False
        user.save()
        # storing username and email as payload in dictionary format
        payload = {
            'username': user.username,
            'email': user.email
        }
        # creating the token
        token = jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')
        print (token,"In the token creation parttttttttttttttttttt")
        currentsite = get_current_site(request)

        try:
            # getting the shortened token using get_surl method
            shortedtoken = get_surl(token)
        except Exception:
            print ("Exception occured in url shortening")
        # converting shortened token to string format

        stringshortedtoken = str(shortedtoken)

        # splitting string
        splittedshortedtokenstr = stringshortedtoken.split('/')

        mail_subject = 'Link to activate the account'
        mail_message = render_to_string('activate.html', {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'token': splittedshortedtokenstr[2],
        })

        recipient_email = os.getenv('EMAILID')

        # sending the mail
        email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
        try:

            email.send()

        except SMTPException as e:
            print(e)
            return HttpResponse(json.dumps("not vaild"))
        print ("outside iffffffffffffffffffffffffffffffffffffffffblock")


        return "success"

