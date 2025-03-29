# Create your views here.
from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse

def donarregistration(request):
    districtdata=tbl_district.objects.all()
    placedata=tbl_place.objects.all()
    if request.method=="POST":
        plc=tbl_place.objects.get(id=request.POST.get('place'))
        tbl_donar.objects.create(donar_name=request.POST.get('donar_name'),
        contact=request.POST.get('contact_no'),
        email=request.POST.get('email'),
        address=request.POST.get('address'),
        gender=request.POST.get('gender'),
        photo=request.FILES.get('photo'),
        proof=request.FILES.get('proof'),
        password=request.POST.get('password'),
        place=plc)
        return render(request,"Guest/DonarRegistration.html",{'district':districtdata,'place':placedata})
    else:
        return render(request,"Guest/DonarRegistration.html",{'district':districtdata,'place':placedata})
   
def recipientregistration(request):
    districtdata=tbl_district.objects.all()
    placedata=tbl_place.objects.all()
    if request.method=="POST":
        plc=tbl_place.objects.get(id=request.POST.get('place'))
        tbl_recipient.objects.create(recipient_name=request.POST.get('recipient_name'),
        contact=request.POST.get('contact_no'),
        email=request.POST.get('email'),
        address=request.POST.get('address'),
        proof=request.FILES.get('proof'),
        password=request.POST.get('password'),
        place=plc)
        return render(request,"Guest/RecipientRegistration.html",{'district':districtdata,'place':placedata})
    else:
        return render(request,"Guest/RecipientRegistration.html",{'district':districtdata,'place':placedata})

def ajax_place(request):
    dist=tbl_district.objects.get(id=request.GET.get('disd'))
    plc=tbl_place.objects.filter(district=dist)
    return render(request,"Guest/AjaxPlace.html",{'PLC':plc})

def login(request):
    if request.method=="POST":
        donarcount=tbl_donar.objects.filter(email=request.POST.get('email'),
                                            password=request.POST.get('password')).count()
        recipientcount=tbl_recipient.objects.filter(email=request.POST.get('email'),
                                            password=request.POST.get('password')).count()
        admincount=tbl_adminlogin.objects.filter(email=request.POST.get('email'),
                                            password=request.POST.get('password')).count()
        if donarcount>0:
            donardata=tbl_donar.objects.get(email=request.POST.get('email'),password=request.POST.get('password'))
            request.session["did"]=donardata.id
            return redirect("Donar:homepage")
        elif recipientcount>0:
            recipientdata=tbl_recipient.objects.get(email=request.POST.get('email'),password=request.POST.get('password'))
            request.session["rid"]=recipientdata.id
            return redirect("Recipient:homepage")
        elif admincount>0:
            admindata=tbl_adminlogin.objects.get(email=request.POST.get('email'),password=request.POST.get('password'))
            request.session["aid"]=admindata.id
            return redirect("Admin:homepage")
        else:
            return redirect("Guest:login")
    else:
        return render(request,"Guest/Login.html")

def ForgetPassword(request):
    
    if request.method=="POST":
        otp=random.randint(10000, 999999)
        request.session["otp"]=otp
        request.session["femail"]=request.POST.get('email')
        send_mail(
            'Respected Sir/Madam ',#subject
            "\rYour OTP for Reset Password Is"+str(otp),#body
            settings.EMAIL_HOST_USER,
            [request.POST.get('email')],
        )
        return redirect("Guest:verification")
    else:
        return render(request,"Guest/ForgetPassword.html")

def OtpVerification(request):
    if request.method=="POST":
        otp=int(request.session["otp"])
        if int(request.POST.get('txtotp'))==otp:
            return redirect("Guest:create")
    return render(request,"Guest/OTPVerification.html")

def CreateNewPass(request):
    if request.method=="POST":
        if request.POST.get('txtpassword2')==request.POST.get('txtpassword3'):
            donarcount=tbl_donar.objects.filter(email=request.session["femail"]).count()
            recipientcount=tbl_recipient.objects.filter(email=request.session["femail"]).count()
            if donarcount>0:
                donar=tbl_donar.objects.get(email=request.session["femail"])
                donar.password=request.POST.get('txtpassword2')
                donar.save()
                return redirect("Guest:login")
            elif recipientcount>0:
                recipient=tbl_recipient.objects.get(email=request.session["femail"])
                recipient.password=request.POST.get('txtpassword2')
                recipient.save()
                return redirect("Guest:login")
            else:
                return redirect("Guest:login")
    else:       
        return render(request,"Guest/CreateNewPassword.html")

def home(request):
    return render(request,"Guest/HomePage.html")

def ajaxemail(request):
    donarcount=tbl_donar.objects.filter(email=request.GET.get("email")).count()
    recipientcount=tbl_recipient.objects.filter(email=request.GET.get("email")).count()
    admincount=tbl_adminlogin.objects.filter(email=request.GET.get("email")).count()
    if donarcount>0 or recipientcount>0 or admincount>0:
        return render(request,"Guest/Ajaxemail.html",{'mess':1})
    else:
         return render(request,"Guest/Ajaxemail.html")

def get_places(request):
    district_id = request.GET.get('district_id')
    places = tbl_place.objects.filter(district_id=district_id).values('id', 'place_name')
    return JsonResponse(list(places), safe=False)