from django.db import models

# Create your models here.
class Img(models.Model):
    imgs= models.URLField(max_length=250)

class Note(models.Model):
    title=models.CharField(max_length=50)
    note=models.TextField()
