from django.db import models
from Recipient.models import *
from Donar.models import *
# Create your models here.
class tbl_applyrequirements(models.Model):
    donar_id=models.ForeignKey(tbl_donar,on_delete=models.CASCADE)
    requirements_id=models.ForeignKey(tbl_requirements,on_delete=models.CASCADE)
    status=models.IntegerField(default=0)

class tbl_paymentrecord(models.Model):
    requirements_id=models.ForeignKey(tbl_requirements,on_delete=models.CASCADE)
    donar_id=models.ForeignKey(tbl_donar,on_delete=models.CASCADE)
    amount=models.CharField(max_length=12)
    date= models.DateField(auto_now_add=True)

class tbl_appointments(models.Model):
    recipient_id=models.ForeignKey(tbl_recipient,on_delete=models.CASCADE)
    donar_id=models.ForeignKey(tbl_donar,on_delete=models.CASCADE)
    date=models.DateField()
    purpose=models.CharField(max_length=100)
    time=models.TimeField()
    status=models.IntegerField(default=0)