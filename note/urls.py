from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns=[
    path('uploadimage',views.UploadImage.as_view(), name='upload_view'),
]