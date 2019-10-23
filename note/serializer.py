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

class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields=['user','title','note','label','image','collab','is_archieve','pin','url']