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


userclassobject=user.UserOperations()

#API for registering the user
class Register(GenericAPIView):
    #setting the serializer class
    serializer_class = UserSerializer


    def post(self, request):

        #calling the register_user method in user.py
        user_registration =userclassobject.register_user(request)
        print (user_registration,"returned to viewssssssssssssssssssssss")
        #string_user_registration=str(user_registration)
        return HttpResponse(json.dumps(user_registration))




#API for login
class Login(GenericAPIView):

    #setting the serializer class
    serializer_class = LoginSerializer
    
    def post(self,request):
        user_login=userclassobject.login_user(request)
        print (user_login,"returned to viewssssssssss")
        return HttpResponse(json.dumps(user_login))



#API for Forgot Password
class ForgotPassword(GenericAPIView):

    #Setting the serializer class
    serializer_class=ForgotPasswordSerializer

    def post(self,request):

        password_forgot = userclassobject.forgot_password(request)
        print (password_forgot,"returned to viewssssssss")
        return HttpResponse(json.dumps(password_forgot))

#API for Reset password
class ResetPassword(GenericAPIView):

    #setting the serializer class
    serializer_class=ResetPasswordSerializer


    def post(self,request,**kwargs):

        #getting the token
        token=kwargs['token']
        # calling the reset_password method inside service
        password_reset = userclassobject.reset_password(request,token)

        print (password_reset)
        return HttpResponse(json.dumps(password_reset))


#API for logout
class Logout(GenericAPIView):

    #setting the serializer class
    serializer_class=LogoutSerializer

    #using 'token_required' decorator
    @token_required
    def post(self,request):
        #calling the logout method inside service
        logout = userclassobject.logout(request)
        print (logout,"returned to viewsssssssssss")
        return HttpResponse(json.dumps(logout))




            

#method for activating the user
def activate(request, token):

    #calling the activate method inside service
    activate = userclassobject.activate(request,token)

    return HttpResponse(json.dumps(activate))


def sociallogin(request):
    return render(request, 'sociallogin.html')

def home(request):
    return render(request, 'home.html')


        
