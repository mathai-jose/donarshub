from django.db import models
from Donar.models import *
from Recipient.models import *

# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)
class tbl_category(models.Model):
    category_name=models.CharField(max_length=50)
class tbl_brand(models.Model):
    brand_name=models.CharField(max_length=50)
class tbl_place(models.Model):
    place_name=models.CharField(max_length=50)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
class tbl_adminlogin(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
class tbl_complaint(models.Model):
    donar=models.ForeignKey(tbl_donar,on_delete=models.SET_NULL,null=True)
    recipient=models.ForeignKey(tbl_recipient,on_delete=models.SET_NULL,null=True)
    title=models.CharField(max_length=50)
    content=models.CharField(max_length=100)
    status=models.IntegerField(default=0)
    reply=models.CharField(max_length=50)
    reply_date=models.DateField(null=True)
    date=models.DateField(auto_now_add=True)
class tbl_feedback(models.Model):
    donar=models.ForeignKey(tbl_donar,on_delete=models.SET_NULL,null=True)
    recipient=models.ForeignKey(tbl_recipient,on_delete=models.SET_NULL,null=True)
    content=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)