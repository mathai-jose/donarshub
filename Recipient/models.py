from django.db import models
from Guest.models import *

# Create your models here.
class tbl_requirements(models.Model):
    recipient_id=models.ForeignKey(tbl_recipient,on_delete=models.CASCADE)
    requirement=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    for_date=models.DateField()
    date_of_post=models.DateField(auto_now_add=True)
    status=models.IntegerField(default=0)

class Chat(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    from_recipient = models.ForeignKey(
        tbl_recipient, on_delete=models.SET_NULL, default=False, null=True, related_name="from_recipient")
    to_recipient = models.ForeignKey(
        tbl_recipient, on_delete=models.SET_NULL, default=False, null=True, related_name="to_recipient")
    from_donar = models.ForeignKey(
        tbl_donar, on_delete=models.SET_NULL, default=False, null=True, related_name="from_donar")
    to_donar = models.ForeignKey(
        tbl_donar, on_delete=models.SET_NULL, default=False, null=True, related_name="to_donar")
    content = models.TextField()

class tbl_events(models.Model):
    recipient_id=models.ForeignKey(tbl_recipient,on_delete=models.CASCADE)
    event_name=models.CharField(max_length=50)
    details=models.CharField(max_length=100)
    date=models.DateField()
    status=models.IntegerField(default=1)