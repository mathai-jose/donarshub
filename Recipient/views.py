# Create your views here.
from django.shortcuts import render,redirect
from Guest.models import *
from Recipient.models import *
from Donar.models import *
from datetime import date
from Admin.models import *        
from django.core.mail import send_mail
from django.conf import settings
def homepage(request):
    if 'rid' in request.session:
        currentdate=date.today()
        print(currentdate)
        datacount=tbl_requirements.objects.filter(for_date__lt=currentdate).count()
        if datacount>0:
            data=tbl_requirements.objects.filter(for_date__lt=currentdate)
            for i  in data:
                i.status=2
                i.save()
        datacount=tbl_events.objects.filter(date__lt=currentdate).count()
        if datacount>0:
            data1=tbl_events.objects.filter(date__lt=currentdate)
            for j  in data1:
                j.status=0
                j.save()
        datacount=tbl_appointments.objects.filter(date__lt=currentdate).count()
        if datacount>0:
            data1=tbl_appointments.objects.filter(date__lt=currentdate)
            for j  in data1:
                j.status=2
                j.save()
            return render(request,"Recipient/HomePage.html")
        else:
            return render(request,"Recipient/HomePage.html")
    else:
        return redirect("Guest:login")
def myprofile(request):
    if 'rid' in request.session:
        data=tbl_recipient.objects.get(id=request.session["rid"])
        return render(request,"Recipient/MyProfile.html",{'data':data})
    else:
        return redirect("Guest:login")
def editprofile(request):
    if 'rid' in request.session:
        data = tbl_recipient.objects.get(id=request.session["rid"])
        districts = tbl_district.objects.all()
        
        if request.method == "POST":
            contact = request.POST.get('contact')
            
            # Validate contact contains exactly 10 digits
            if not contact.isdigit() or len(contact) != 10:
                return render(request, "Recipient/EditProfile.html", {
                    'data': data,
                    'districts': districts,
                    'error': "Contact must be exactly 10 digits"
                })
            
            data.recipient_name = request.POST.get('recipient_name')
            data.contact = contact
            data.email = request.POST.get('email')
            data.address = request.POST.get('address')
            
            # Get place object and update recipient's location
            place_id = request.POST.get('place')
            if place_id:
                place = tbl_place.objects.get(id=place_id)
                data.place = place
            
            data.save()
            return redirect('Recipient:editprofile')
        
        return render(request, "Recipient/EditProfile.html", {
            'data': data,
            'districts': districts
        })
    else:
        return redirect("Guest:login")

def changepswd(request):
    if 'rid' in request.session:
        if request.method=="POST":
            recipientcount=tbl_recipient.objects.filter(id=request.session["rid"],password=request.POST.get('pswd')).count()
            if recipientcount>0:
                if request.POST.get('new_pswd')==request.POST.get('c_pswd'):
                    recipientdata=tbl_recipient.objects.get(id=request.session["rid"])
                    recipientdata.password=request.POST.get('new_pswd')
                    recipientdata.save()
                    return redirect("Recipient:homepage")
                else:
                    return render(request,"Recipient/ChangePassword.html")
            else:
                return render(request,"Recipient/ChangePassword.html")
        else:
            return render(request,"Recipient/ChangePassword.html")
    else:
        return redirect("Guest:login")

def requirements(request):
    if 'rid' in request.session:
        recipientid=tbl_recipient.objects.get(id=request.session["rid"])
        requirementsdata=tbl_requirements.objects.filter(recipient_id=request.session["rid"]).exclude(status=4)
        if request.method=="POST":
            # recipient_id=tbl_recipient.objects.get(id=request.POST.get('recipient_id'))
            tbl_requirements.objects.create(recipient_id=recipientid,
            details=request.POST.get('details'),requirement=request.POST.get('requirements'),for_date=request.POST.get('for_date'))
            return render(request,"Recipient/Requirements.html",{'requirements':requirementsdata})
        else:
            return render(request,"Recipient/Requirements.html",{'requirements':requirementsdata})
    else:
        return redirect("Guest:login")

def editrequirement(request,rid):
    if 'rid' in request.session:
        data = tbl_requirements.objects.filter(id=rid).exclude(status=4).first()
        if request.method=="POST":
            if data:
                data.requirement = request.POST.get('requirements')
                data.details = request.POST.get('details')
                for_date = request.POST.get('for_date')
                if for_date:  # Only update if date is provided
                    data.for_date = for_date
                data.save()
                return redirect("Recipient:requirements")
            else:
                return redirect("Recipient:requirements")
        else:
            return render(request,"Recipient/Requirements.html",{'data':data})
    else:
        return redirect("Guest:login")

def deleterequirement(request,rid):
    tbl_requirements.objects.get(id=rid).delete()
    return redirect("Recipient:requirements")

def acceptrequirement(request,aid):
    data=tbl_requirements.objects.get(id=aid)
    data.status=1
    data.save()
    return redirect("Recipient:requirements")
def rejectrequirement(request,rid):
    data=tbl_requirements.objects.get(id=rid)
    data.status=2
    data.save()
    return redirect("Recipient:requirements")

def donaracceptance(request):
    if 'rid' in request.session:
        recipent=tbl_recipient.objects.get(id=request.session["rid"])
        acceptance=tbl_applyrequirements.objects.filter(requirements_id__recipient_id=recipent).exclude(status=3)
        return render(request,"Recipient/DonarAcceptance.html",{'data':acceptance})
    else:
        return redirect("Guest:login")

def confirmacceptance(request,cid):
    data=tbl_applyrequirements.objects.get(id=cid)
    data.status=1
    data.save()
    return redirect("Recipient:donaracceptance")
def rejectacceptance(request,rid):
    data=tbl_applyrequirements.objects.get(id=rid)
    data.status=2
    data.save()
    return redirect("Recipient:donaracceptance")

def acceptconfirmlist(request):
    data=tbl_applyrequirements.objects.filter(status=1)
    return render(request,"Recipient/AcceptConfirmList.html",{'data':data})

def acceptrejectlist(request):
    data=tbl_applyrequirements.objects.filter(status=2)
    return render(request,"Recipient/AcceptRejectList.html",{'data':data})

def delivered(request,did):
    if 'rid' in request.session:
        data=tbl_applyrequirements.objects.get(id=did)
        name=data.donar_id.donar_name
        email=data.donar_id.email
        req=data.requirements_id.id
        reqdata=tbl_requirements.objects.get(id=req)
        reqname=reqdata.requirement
        send_mail(
                'Respected Sir/Madam '+name,#subject
                "\rOur  Requirement "+reqname+"Is Delivered SuccessFully....\rThank You for your great generosity",#body
                settings.EMAIL_HOST_USER,
                [email],
            )
        data.status=3
        data.save()
        return redirect("Recipient:donaracceptance")
    else:
        return redirect("Guest:login")
def deliveredlist(request):
    if 'rid' in request.session:
        data=tbl_applyrequirements.objects.filter(requirements_id_id=request.session["rid"],status=3)
        return render(request,"Recipient/DeliveredList.html",{'data':data})
    else:
        return redirect("Guest:login")

def viewdonardetails(request):
    if 'rid' in request.session:
        districtdata=tbl_district.objects.all()
        placedata=tbl_place.objects.all()
        data=tbl_donar.objects.filter().exclude(status=0)
        return render(request,"Recipient/ViewDonarDetails.html",{'data':data,'district':districtdata,'place':placedata})
    else:
        return redirect("Guest:login")

def ajaxdonor(request):
    if request.GET.get("pid")!="":
        placedata=tbl_place.objects.get(id=request.GET.get('pid'))
        data=tbl_donar.objects.filter(place=placedata)
        return render(request,"Recipient/Ajaxdonor.html",{'data':data})
    else:
        districtdata=tbl_district.objects.get(id=request.GET.get('did'))
        data=tbl_donar.objects.filter(place__district=districtdata)
        return render(request,"Recipient/Ajaxdonor.html",{'data':data})


def chatuser(request, cid):
    if 'rid' in request.session:
        chatobj = tbl_donar.objects.get(id=cid)
        if request.method == "POST":
            cied = request.POST.get("cid")
            # print(cied)
            ciedobj = tbl_donar.objects.get(id=cied)
            sobj = tbl_recipient.objects.get(id=request.session["rid"])
            content = request.POST.get("msg")
            # print(cied)
            # print(content)
            Chat.objects.create(
                from_recipient=sobj, to_donar=ciedobj, content=content, from_donar=None, to_recipient=None)
            return render(request, 'Recipient/Chat.html', {"chatobj": chatobj})
        else:
            return render(request, 'Recipient/Chat.html', {"chatobj": chatobj})
    else:
        return redirect("Guest:login")

def loadchatuser(request):
    if 'rid' in request.session:
        cid = request.GET.get("cid")
        request.session["cid"] = cid
        cid1 = request.session["cid"]
        # print(cid1)
        # print(cid)
        shopobj = tbl_donar.objects.get(id=cid)
        # print(userobj)
        sid = request.session["rid"]
        # print(sid)
        suserobj = tbl_recipient.objects.get(id=request.session["rid"])
        # chatobj1 = Chat.objects.filter(Q(to_user=suserobj) | Q(
        #     from_user=suserobj), Q(to_shop=shopobj) | Q(from_shop=shopobj))
        # print(chatobj1)  # send message
        # print(chatobj2)  # recived msg
        chatobj = Chat.objects.raw(
            "select * from Recipient_chat c inner join Guest_tbl_recipient u on (u.id=c.from_recipient_id) or (u.id=c.to_recipient_id) WHERE  c.from_donar_id=%s or c.to_donar_id=%s order by c.date", params=[(cid1), (cid1)])
        print(chatobj.query)
        return render(request, 'Recipient/Load.html', {"obj": chatobj, "sid": sid, "shop": shopobj, "userobj": suserobj})
    else:
        return redirect("Guest:login")

def viewpayments(request):
    if 'rid' in request.session:
        data=tbl_paymentrecord.objects.filter(requirements_id__recipient_id=request.session["rid"])
        return render(request,'Recipient/ViewPayments.html', {'data':data})
    else:
        return redirect("Guest:login")

def events(request):
    if 'rid' in request.session:
        currentdate=date.today()
        datacount=tbl_events.objects.filter(date__lt=currentdate).count()
        if datacount>0:
            data1=tbl_events.objects.filter(date__lt=currentdate)
            for j  in data1:
                j.status=0
                j.save()
        data=tbl_events.objects.filter(recipient_id=request.session["rid"])
        if request.method=="POST":
            ename=request.POST.get('event_name')
            det=request.POST.get('details')
            datetime=request.POST.get('date')
            rid=tbl_recipient.objects.get(id=request.session["rid"])
            tbl_events.objects.create(recipient_id=rid,event_name=ename,details=det,date=datetime)
            return render(request,"Recipient/Events.html",{'data':data})
        else:
            return render(request,"Recipient/Events.html",{'data':data})
    else:
        return redirect("Guest:login")

def editevent(request,eid):
    data=tbl_events.objects.get(id=eid)
    if request.method=="POST":
        data.event_name=request.POST.get('event_name')
        data.details=request.POST.get('details')
        data.date=request.POST.get('date')
        data.save()
        return redirect("Recipient:events")
    else:
        return render(request,"Recipient/EditEvent.html",{'data':data})

def deleteevent(request,did):
    data=tbl_events.objects.get(id=did)
    data.status=0
    data.save()
    return redirect("Recipient:events")

def viewappointments(request):
    if 'rid' in request.session:
        data=tbl_appointments.objects.filter(recipient_id=request.session["rid"] )
        return render(request,"Recipient/ViewAppointments.html",{'data':data})  
    else:
            return redirect("Guest:login")

def acceptappointment(request,aid):
    data=tbl_appointments.objects.get(id=aid)
    data.status=1
    data.save()
    return redirect("Recipient:viewappointments")

def denyappointment(request,did):
    data=tbl_appointments.objects.get(id=did)
    data.status=2
    data.save()
    return redirect("Recipient:viewappointments")

def acceptedappointments(request):
    data=tbl_appointments.objects.filter(recipient_id=request.session["rid"],status=1 )
    return render(request,"Recipient/AcceptedAppointments.html",{'data':data})  

def visitedappointment(request,vid):
    data=tbl_appointments.objects.get(id=vid )
    data.status=3
    data.save()
    return redirect("Recipient:acceptedappointments")  

def viewvisiters(request):
    if 'rid' in request.session:
        data=tbl_appointments.objects.filter(status=3,recipient_id=request.session["rid"])
        return render(request,"Recipient/ViewVisiters.html",{'data':data})
    else:
            return redirect("Guest:login")

def complaint(request):
    if 'rid' in request.session:
        if request.method=="POST":
            rid=tbl_recipient.objects.get(id=request.session["rid"])
            tbl_complaint.objects.create(recipient=rid,title=request.POST.get('title'),content=request.POST.get('content'))
            return redirect("Recipient:homepage")
        else:
            return render(request,"Recipient/Complaint.html")
    else:
        return redirect("Guest:login") 

def reply(request):
    if 'did' in request.session:
        rid=tbl_recipient.objects.get(id=request.session["rid"])
        data=tbl_complaint.objects.filter(recipient=rid)
        return render(request,"Recipient/ViewReply.html",{'data':data})    
    else:
        return redirect("Guest:login") 

def feedback(request):
    if 'did' in request.session:
        if request.method=="POST":
            rid=tbl_recipient.objects.get(id=request.session["rid"])
            tbl_feedback.objects.create(recipient=rid,content=request.POST.get('feedback'))
            return redirect("Recipient:homepage")
        else:
            return render(request,"Recipient/feedback.html")
    else:
        return redirect("Guest:login") 

def logout(request):
    del request.session["rid"]
    return redirect("Guest:home")