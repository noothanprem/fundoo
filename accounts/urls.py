from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns=[
    path('login',views.Login.as_view(), name='login_view'),
    path('register',views.Register.as_view(), name='register_view'),
    path('activate/<token>/',views.activate,name='activate'),
    path('forgotpassword',views.ForgotPassword.as_view(),name='forgotpassword_view'),
    #path('<Token>/', views.verify, name='verify'),
    path('resetpassword/<token>/', views.ResetPassword.as_view(), name='resetpassword'),
]