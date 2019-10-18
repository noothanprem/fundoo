from rest_framework import serializers
from .models import Img
from .models import Note
class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Img
        fields=['imgs']

class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields=['title','note']