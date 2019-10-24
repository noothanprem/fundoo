from rest_framework import serializers
from .models import Img,Note,Label
class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Img
        fields=['imgs']

class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields=['title','note']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields='__all__'

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Label
        fields='__all__'