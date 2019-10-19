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
from .redisfunc import RedisOperations
from .decorators import token_required
import redis
from .redisfunc import RedisOperations
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

#API for registering the user
class Register(GenericAPIView):
    #setting the serializer class
    serializer_class = UserSerializer


    def post(self, request):

        #getting the username,email and password
        username=request.data['username']
        email=request.data['email']
        password=request.data['password']

        #checking whether the user name or email exists or not
        if ((User.objects.filter(username=username).exists()) or (User.objects.filter(email=email).exists())):
            
            return HttpResponse(json.dumps({"message":"Username or email is already taken"}),status=404)
        #checking whether any field is empty or not
        elif username=="" or password=='' or email=='':
            
            return HttpResponse(json.dumps({"message":"Username or email is empty"}),status=404)
        else:
            try:

                #Inserting a new row into the database
                user = User.objects.create_user(username=username, email=email, password=password)
            except ObjectDoesNotExist as e:
                print(e)
            
            user.save()
            user.is_active = False
            user.save()
            #storing username and email as payload in dictionary format
            payload = {
                'username': user.username,
                'email': user.email
            }
            #creating the token
            token = jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')

            currentsite = get_current_site(request)
            
            #getting the shortened token using get_surl method
            shortedtoken=get_surl(token)
            #converting shortened token to string format
            stringshortedtoken=str(shortedtoken)
            #splitting string
            splittedshortedtokenstr=stringshortedtoken.split('/')
            
            
            mail_subject='Link to activate the account'
            mail_message = render_to_string('activate.html', {
                'user': user.username,
                'domain': get_current_site(request).domain,
                'token': splittedshortedtokenstr[2],
            })


            recipient_email=['noothan627@gmail.com']

            #sending the mail
            email=EmailMessage(mail_subject, mail_message, to=[recipient_email])
            try:

                email.send()
                    
            except SMTPException as e:
                print(e)
                return HttpResponse(json.dumps("not vaild"))

            return HttpResponse(json.dumps({"message":"Please check your mail for activating"}))
        
        return HttpResponse(json.dumps("not vaild"),status=404)


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
            smddata['data'] = [key]

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
            try
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
            headerlist=header.split(" ")
            token=headerlist[1]
        except Exception:
            print ("Exception occured while getting the request header")
        #r = redis.StrictRedis(host='localhost', port=6379, db=0)
        try:
            ro=RedisOperations()
        except Exception:
            print ("Exception occured while creating object")
        r=ro.r
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


        
