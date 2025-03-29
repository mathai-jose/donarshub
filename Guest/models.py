from django.db import models
from Admin.models import *

# Create your models here.
class tbl_donar(models.Model):
    donar_name=models.CharField(max_length=50)
    contact=models.CharField(max_length=12)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    place=models.ForeignKey("Admin.tbl_place",on_delete=models.CASCADE)
    gender=models.CharField(max_length=10)
    photo=models.FileField(upload_to='docs/')
    proof=models.FileField(upload_to='docs/')
    password=models.CharField(max_length=50)
    status=models.IntegerField(default=0)

class tbl_recipient(models.Model):
    recipient_name=models.CharField(max_length=50)
    contact=models.CharField(max_length=12)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    place=models.ForeignKey("Admin.tbl_place",on_delete=models.CASCADE)
    proof=models.FileField(upload_to='docs/')
    password=models.CharField(max_length=50)