from django.db import models

# Create your models here.

class Userdetails(models.Model):
    username = models.CharField(max_length=25)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30,unique=True,null=True)
    password = models.CharField(max_length=30, default='default_password')