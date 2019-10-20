# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .serializers import UserSerializer,LoginSerializer, ForgotPasswordSerializer,ResetPasswordSerializer,LogoutSerializer
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
import templates
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from .decorators import token_required
import redis
from .Lib.redisfunc import RedisOperations
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist



from accounts.service import user

#API for registering the user
class Register(GenericAPIView):
    #setting the serializer class
    serializer_class = UserSerializer


    def post(self, request):

        #calling the register_user method in user.py
        user_registration = user.register_user(request)
        #return success message if the methurned returns success or else, return failure message

        message = {
            "message": "",
        }

        if(user_registration == "success"):

            return HttpResponse(user_registration)
        else:

            return HttpResponse(user_registration)




#API for login
class Login(GenericAPIView):

    #setting the serializer class
    serializer_class = LoginSerializer
    
    def post(self,request):

        #getting the username and password
        username=request.data['username']
        password=request.data['password']

        if username == "" or password == '' :
            return HttpResponse(json.dumps({"message": "Username or Password is empty"}), status=404)
        # Used to store the data in SMD(success,message,data) format
        smddata = {
            'success': False,
            'message': '',
            'data': []
        }

        try:
            user = auth.authenticate(username=username, password=password)
        except PermissionDenied as e:
            print(e)

        if user is not None:
        
            try:
                auth.login(request, user)
            except PermissionDenied as e:
                print(e)

            try:
                user=request.user
            except ObjectDoesNotExist as e:
                print (e)

            try:
                payload = {
                'username': json.dumps(username),
                }
            except Exception:
                print ("json operation failed")
            #z=json.dumps(payload)
            
            token = jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')
            
            ro=RedisOperations()
            ro.save(token)
            # Token = jwt_token['token']

            #Sendin the response in Success Message Data(SMD) format
            smddata['success'] = True
            smddata['message'] = "Login Successful"
            smddata['data'] = [token]

            try:
                response=HttpResponse(json.dumps(smddata))
            except Exception:
                print ("json operaion failed")
            return response

        else:
            return HttpResponse('Login Failed',status=404)


#API for Forgot Password
class ForgotPassword(GenericAPIView):

    #Setting the serializer class
    serializer_class=ForgotPasswordSerializer

    def post(self,request):

        #getting the emailid
        emailid = request.data['email']

        if emailid == '':

            return HttpResponse(json.dumps({"message": "email is empty"}), status=404)


        #checking whether the user exists in the database or not
        if User.objects.filter(email=emailid).exists():
            try:
                #getting that user object
                u = User.objects.get(email=emailid)
            except ObjectDoesNotExist as e:
                print (e)


            #storing the username and email as payload
            payload = {
                'username': u.username,
                'email': u.email
            }

            #generating the jwt token
            try:
                jwt_token = {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}
            except Exception :
                print("EXception occured while generating the token")

            token = jwt_token["token"]


            currentsite = get_current_site(request)
            subject = "Link to Reset the password"
            message = render_to_string('forgotpassword.html', {
                'domain':"http://127.0.0.1:8000",
                'token':token
            })

            #sending the mail
            try:
                send_mail(subject, message, 'noothanprem@gmail.com', ['noothan627@gmail.com'])
            except SMTPException as e:
                print(e)

            return HttpResponse('Check your mail for the link')
                #return render(request, "accounts/resetmail.html")

        else:
            return HttpResponse('Invalid Email id.. Try Once again',status=404)
                

#API for Reset password
class ResetPassword(GenericAPIView):

    #setting the serializer class
    serializer_class=ResetPasswordSerializer


    def post(self,request,**kwargs):

        token=kwargs['token']

        #decoding the token and storing it into user_details
        user_details = jwt.decode(token, "secret")
        #getting the username from token
        user_name = user_details['username']
        try:
            #getting the user object
            u = User.objects.get(username=user_name)
        except ObjectDoesNotExist as e:
            print(e)

        if u is not None:
            #Taking the new password two times
            password = request.data['password']
        else:
            return HttpResponse('Invalid User',status=404)
        
        #checking whether the user wxists in the database or not
        if User.objects.filter(username=user_name).exists():
            #getting that user object
            try:
                user1 = User.objects.get(username=user_name)
            except ObjectDoesNotExist as e:
                print (e)
            #setting the password to new password
            try:
                user1.set_password(password)
            except Exception:
                print ("Exception occured while setting the password")

            try:
                #saving the user
                user1.save()
            except PermissionDenied as e:
                print (e)

            return HttpResponse('Passsword Changed Successfully')

        else:

            #If two passwords are not same, display passords doesn't match
            return HttpResponse("Both the Passwords doesn't match",status=404)
    #return render(request, 'accounts/resetpassword.html')


#API for logout
class Logout(GenericAPIView):

    #setting the serializer class
    serializer_class=LogoutSerializer

    #using 'token_required' decorator
    @token_required
    def post(self,request):

        try:
            #getting the request header
            header=request.META['HTTP_AUTHORIZATION']
            print (header,"hwhrhrhrhrhrhrhrhhrhrhhrhrhh")
            headerlist=header.split(" ")
            token=headerlist[1]
        except Exception:
            print ("Exception occured while getting the request header")

        #creating the object for RedisOperations class
        try:
            redis_object=RedisOperations()
        except Exception:
            print ("Exception occured while creating object")

        r=redis_object.r
        #deleting the token from redis
        r.delete(token)

        return HttpResponse("Logout Successful")
            

            

#method for activating the user
def activate(request, token):

    try:
        #getting the token after shortening the URL
        expandedtoken=ShortURL.objects.get(surl=token)
    except Exception:
        print ("Exception occured while expanding the URL")
    print(expandedtoken.lurl)
    #decoding the token and getting the datas
    user_details = jwt.decode(expandedtoken.lurl, 'secret', algorithms='HS256')
    #getting the user name
    user_name = user_details['username']
    
    try:
        #getting the user object
        user1 = User.objects.get(username=user_name)
        
    except ObjectDoesNotExist as e:
        print(e)

    if user1 is not None:
        #Making is_active flag true
        user1.is_active = True
        #saving the user
        user1.save()
        return HttpResponse("Registration Successful",status=404)
    else:
        return HttpResponse('Registration Failed',status=404)


def logins(request):
    return render(request, 'sociallogin.html')

def home(request):
    return render(request, 'home.html')


        
