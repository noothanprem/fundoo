from rest_framework import serializers
from .models import Img, Note, Label


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['imgs']


class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'note']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title','note','label','collab','image','is_archieve','is_trash','reminder','pin','url']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
