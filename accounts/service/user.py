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
from django_short_url.models import ShortURL
import os
from accounts.Lib.redisfunc import RedisOperations
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

class UserOperations:

    def register_user(self,request):

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
            response={"message": "Username or email alredy exists"}
            return response

        # checking whether any field is empty or not
        elif username == "" or password == '' or email == '':
            response={"message": "Username or email is empty"}
            return response
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
            print (shortedtoken,"shooorteddd tokennnnnnnnnnnnnnnn")
            stringshortedtoken = str(shortedtoken)

            # splitting string
            splittedshortedtokenstr = stringshortedtoken.split('/')
            print (splittedshortedtokenstr[2],"splittedshotedtokennnnnnnnnnnnnnnn")
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
                response={"message":"email id not valid"}
                return response
            print ("outside iffffffffffffffffffffffffffffffffffffffffblock")

            response = {"message": "Please check your mail for activating"}
            return response


    def login_user(self,request):
        # getting the username and password
        username = request.data['username']
        password = request.data['password']
        print (username,"userrrrrrrrrrnameeeeeeeeeinloginuserr")
        if username == "" or password == '':
            response={"message":"Username or Password is empty"}
            return response
        # Used to store the data in SMD(success,message,data) format
        smddata = {
            'success': False,
            'message': '',
            'data': []
        }
        print ("Before authenticaaateeeeee")
        try:
            user = auth.authenticate(username=username, password=password)
            print (user)
        except PermissionDenied as e:
            print(e)
        print (user,"userrrrrrrrrrrrrrrrrrrrrr")

        if user is not None:

            try:
                auth.login(request, user)
            except PermissionDenied as e:
                print(e)
            print ("After loginnnnnnnnnnnnnnnnnnnnnauth")

            print ("Inside payloaaaaaddddddddddddd")
            payload = {
                'username': json.dumps(username),
            }

            print ("After payloaaaaaadddddddddddddddddd")
            # z=json.dumps(payload)
            print ("before token generationnnnnnnnnnn")
            token = jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')
            print ("After token generationnnnnnnnnnn")
            print(token,"Inside token rediiiiiisssssssssssssssss")
            ro = RedisOperations()
            ro.save(token)
            print ("After Redis operationsssssssssssss")
            # Token = jwt_token['token']

            # Sending the response in Success Message Data(SMD) format
            smddata['success'] = True
            smddata['message'] = "Login Successful"
            smddata['data'] = [token]
            response = {"message": "Login Success"}
            return response
        else:
            response = {"message": "Login Failed"}
            print ("Login failed at lastttttttttttttttttt")
            return response


    def forgot_password(self,request):

        # getting the emailid
        emailid = request.data['email']
        print (emailid,"emaillllllllllllllllllllllllllllllllllllidddd")
        if emailid == '':
            response = {"message": "email is empty"}
            return response

        # checking whether the user exists in the database or not
        if User.objects.filter(email=emailid).exists():
            print ("emaillllll existsssssssssssssssssssssssss")
            try:
                # getting that user object
                user = User.objects.get(email=emailid)
            except ObjectDoesNotExist as e:
                print (e)
            print ("After gettting the userrrrrrrrrr")

            # storing the username and email as payload
            payload = {
                'username': user.username,
                'email': user.email
            }
            print ("Afterrrrr payloadddddddddddd")
            # generating the jwt token
            try:
                jwt_token = {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}
            except Exception:
                print("EXception occured while generating the token")
            print("Afterrrrr token generationnnnnnn")
            token = jwt_token["token"]

            currentsite = get_current_site(request)
            subject = "Link to Reset the password"
            print ("Before rendering templateeeeeeeeeeeeeeeeee")
            message = render_to_string('forgotpassword.html', {
                'domain': "http://127.0.0.1:8000",
                'token': token
            })
            print ("Before sendmaillllllllllllllllll")
            # sending the mail
            try:
                send_mail(subject, message, 'noothanprem@gmail.com', ['noothan627@gmail.com'])
            except SMTPException as e:
                print(e)
            print("Afterrrrr send maillllllllllllllllll")
            response = {"message": "Check your mail for the link"}
            return response
            # return render(request, "accounts/resetmail.html")

        else:
            print ("mailid is invaliddddddddddddddddddddddddd")
            response = {"message": "Invalid Email id.. Try Once again"}
            return response


    def reset_password(self,request,token):

        # decoding the token and storing it into user_details
        user_details = jwt.decode(token, "secret")
        # getting the username from token
        user_name = user_details['username']
        try:
            # getting the user object
            u = User.objects.get(username=user_name)
        except ObjectDoesNotExist as e:
            print(e)

        if u is not None:
            # Taking the new password two times
            password = request.data['password']
        else:
            return "Invalid User"

        # checking whether the user wxists in the database or not
        if User.objects.filter(username=user_name).exists():
            # getting that user object
            try:
                user = User.objects.get(username=user_name)
            except ObjectDoesNotExist as e:
                print (e)
            # setting the password to new password
            try:
                user.set_password(password)
            except Exception:
                print ("Exception occured while setting the password")

            try:
                # saving the user
                user.save()
            except PermissionDenied as e:
                print (e)
            response = {"message": "Passsword Changed Successfully"}
            return response

        else:

            # If two passwords are not same, display passords doesn't match
            response = {"message": "Both the Passwords doesn't match"}
            return response

    def logout(self,request):

        try:
            # getting the request header
            header = request.META['HTTP_AUTHORIZATION']
            print (header, "hwhrhrhrhrhrhrhrhhrhrhhrhrhh")
            headerlist = header.split(" ")
            token = headerlist[1]
        except Exception:
            print ("Exception occured while getting the request header")
            response = {"message": "Logout Failed"}
            return response


        # creating the object for RedisOperations class
        try:
            redis_object = RedisOperations()
        except Exception:
            print ("Exception occured while creating object")
            response = {"message": "Logout Failed"}
            return response
        try:
            r = redis_object.r
            # deleting the token from redis
            r.delete(token)
        except Exception:
            response = {"message": "Logout Failed"}
            return response
        response = {"message": "Logout Successful"}
        return response


    def activate(self,request,token):

        try:
            # getting the token after shortening the URL
            expandedtoken = ShortURL.objects.get(surl=token)
        except Exception:
            print ("Exception occured while expanding the URL")
            response = {"message": "User activation failed"}
            return response
        print(expandedtoken.lurl)
        # decoding the token and getting the datas
        user_details = jwt.decode(expandedtoken.lurl, 'secret', algorithms='HS256')
        # getting the user name
        user_name = user_details['username']

        try:
            # getting the user object
            user1 = User.objects.get(username=user_name)

        except ObjectDoesNotExist as e:
            print(e)
            response = {"message": "User activation failed"}
            return response

        if user1 is not None:
            # Making is_active flag true
            user1.is_active = True
            # saving the user
            user1.save()
            response = {"message": "Registration Successful"}
            return response

        else:
            response = {"message": "Registration Failed"}
            return response
