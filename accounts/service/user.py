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
import os
from jwt.exceptions import DecodeError
from redis.exceptions import ConnectionError,AuthenticationError

class UserOperations:

    def smd_response(self,success,message,data):
        response={
            "success":"",
            "message":"",
            "data":""
        }
        response['success']=success
        response['message']=message
        response['data']=data
        return response

    def register_user(self,request):

        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']



            message={
                "success":"",
                "message":"",
                "data":""
            }

            # checking whether the user name or email exists or not
            if ((User.objects.filter(username=username).exists()) or (User.objects.filter(email=email).exists())):

                response = self.smd_response(False, 'Username or email alredy exists', '')
                return response

            # checking whether any field is empty or not
            elif username == "" or password == '' or email == '':

                response = self.smd_response(False, 'Username or email is empty', '')
                return response
            else:



                # Inserting a new row into the database
                user = User.objects.create_user(username=username, email=email, password=password)

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


                # getting the shortened token using get_surl method
                shortedtoken = get_surl(token)

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

                email.send()
                response = self.smd_response(True, 'Please check your mail for activating', '')
                return response
        except SMTPException:
            response=self.smd_response(False,'Exception while sending mail','')
        except user.DoesNotExist:
            response = self.smd_response(False, 'Exception while getting the user using filter', '')
        except DecodeError:
            response = self.smd_response(False, 'Exception while generating the token', '')


        return response


    def login_user(self,request):

        try:

            # getting the username and password
            username = request.data['username']
            password = request.data['password']

            if username == "" or password == '':
                print ("before user name empty responseeeeeeeeeeeeee")
                response = self.smd_response(False, 'Username or Password is empty', '')
                print (response,"after user name empty responseeeeeeeeeeeeee")
                return response

            # Used to store the data in SMD(success,message,data) format
            smddata = {
                'success': False,
                'message': '',
                'data': []
            }

            print ("before authenticating user...................")
            user = auth.authenticate(username=username, password=password)
            print(user, "After authenticating userrrrrrrrrrrrrrrrrrr")




            if user is not None:
                print ("Before logging innnnnnnnnnnnnnnnn")
                auth.login(request, user)


                payload = {
                    'username': json.dumps(username),
                }


                # z=json.dumps(payload)
                print ("Before generating the tokennnnnnnnnnnnnnnn")
                token = jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')

                print (token,"After generating tokennnnnnnnnnnnn")
                ro = RedisOperations()
                ro.save(token)


                response = self.smd_response(True, 'Login Success', token)
                print (response,"After redis operations")
                return response
            else:

                response = self.smd_response(False, 'Login Failed', '')
                print (response,"Inside else bodyyyyyyyyyyyyyy")
                return response
        except DecodeError:
            response = self.smd_response(False, 'Exception while generating token', '')
            print (response,"Decode Errorrrrrrrrrrrrrrr")
        except PermissionDenied:
            response = self.smd_response(False, 'Exception while authenticating user', '')
            print (response,"PermissionDeniedddddddd")
        except ConnectionError:
            response = self.smd_response(False, 'Exception in redis operation-ConnectionError', '')
            print (response,"ConnectionErrorrrrrrrrrrr")
        except AuthenticationError:
            response = self.smd_response(False, 'Exception in redis operation-AuthenticationError', '')
            print(response,"Authentication errorrrrrrrrrr")

        return response


    def forgot_password(self,request):

        try:

            # getting the emailid
            emailid = request.data['email']

            if emailid == '':

                response = self.smd_response(False, 'email is empty', '')
                return response

            user = User.objects.get(email=emailid)
            # checking whether the user exists in the database or not
            if user is not None:


                # storing the username and email as payload
                payload = {
                    'username': user.username,
                    'email': user.email
                }

                # generating the jwt token
                jwt_token = {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}

                token = jwt_token["token"]

                currentsite = get_current_site(request)
                subject = "Link to Reset the password"

                message = render_to_string('forgotpassword.html', {
                    'domain': "http://127.0.0.1:8000",
                    'token': token
                })
                sender=os.getenv('EMAIL_HOST_USER')
                reciever=os.getenv('EMAILID')

                # sending the mail

                send_mail(subject, message, sender, [reciever])


                response = self.smd_response(True, 'Check your mail for the link', '')
                return response


            else:


                response = self.smd_response(False, 'Invalid Email id.. Try Once again', '')
                return response
        except SMTPException:
            response = self.smd_response(False, 'Exception occured while sending email', '')
        except DecodeError:
            response = self.smd_response(False, 'Exception occured while generating token', '')
        except user.DoesNotExist:
            response = self.smd_response(False, 'Exception occured while getting the user object', '')


    def reset_password(self,request,token):

        try:

            # decoding the token and storing it into user_details
            user_details = jwt.decode(token, "secret")
            # getting the username from token
            user_name = user_details['username']
            # getting the user object
            u = User.objects.get(username=user_name)


            if u is not None:
                # Taking the new password two times
                password = request.data['password']
            else:
                response = self.smd_response(False, 'Invalid User', '')
                return response

            # checking whether the user wxists in the database or not
            user = User.objects.get(username=user_name)
            if user is not None:
                # getting that user object
                # setting the password to new password

                user.set_password(password)


                # saving the user
                user.save()
                response = self.smd_response(True, 'Passsword Changed Successfully', '')

                return response

            else:

                # If two passwords are not same, display passords doesn't match
                response = self.smd_response(False, 'Both the Passwords doesnt match', '')

                return response
        except user.DoesNotExist:
            response = self.smd_response(False, 'Exception occured while accessing the user object', '')
        except DecodeError:
            response = self.smd_response(False, 'Exception occured while generating the token', '')
        return response

    def logout(self,request):

        try:
            # getting the request header
            header = request.META['HTTP_AUTHORIZATION']
        
            headerlist = header.split(" ")
            token = headerlist[1]
        


            # creating the object for RedisOperations class

            redis_object = RedisOperations()

            r = redis_object.r
            # deleting the token from redis
            r.delete(token)

            response = self.smd_response(True, 'Logout Successful', '')
            return response
        except ConnectionError:
            response = self.smd_response(False, 'Exception occured while accessing redis-ConnectionError', '')
        except AuthenticationError:
            response = self.smd_response(False, 'Exception occured while accessing redis-AuthenticationError', '')
        return response


    def activate(self,request,token):

        try:
            # getting the token after shortening the URL
            expandedtoken = ShortURL.objects.get(surl=token)

            print(expandedtoken.lurl)
            # decoding the token and getting the datas
            user_details = jwt.decode(expandedtoken.lurl, 'secret', algorithms='HS256')
            # getting the user name
            user_name = user_details['username']

            # getting the user object
            user1 = User.objects.get(username=user_name)


            if user1 is not None:
                # Making is_active flag true
                user1.is_active = True
                # saving the user
                user1.save()
                response = self.smd_response(True, 'Registration Successful', '')
                return response

            else:
                response = self.smd_response(False, 'Registration Failed', '')

                return response
        except User.DoesNotExist:
            response = self.smd_response(False, 'Exception occurred while getting the user object', '')
        except DecodeError:
            response = self.smd_response(False, 'Exception occurred while decoding the token', '')
        return response
