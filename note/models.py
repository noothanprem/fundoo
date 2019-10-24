from django.db import models
from django.contrib.auth.models import User
from colorful.fields import RGBColorField

# Create your models here.
class Img(models.Model):
    imgs= models.URLField(max_length=250)

class Label(models.Model):
    name = models.CharField(max_length=100,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='labeluser')


class Note(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='noteuser')
    title=models.CharField(max_length=50)
    note=models.TextField()
    label=models.ManyToManyField(Label,blank=True,related_name='label')
    collab=models.ManyToManyField(User,blank=True,related_name='collab')
    image=models.ImageField(blank=True)
    is_archieve=models.BooleanField(default=False)
    pin=models.BooleanField(default=False)
    url=models.URLField(blank=True)


