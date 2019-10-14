from django.db import models

# Create your models here.
class Img(models.Model):
    imgs= models.URLField(max_length=250)