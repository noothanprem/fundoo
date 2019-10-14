from rest_framework import serializers
from .models import Img
class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Img
        fields=['imgs']