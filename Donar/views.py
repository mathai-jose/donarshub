from django.shortcuts import render,redirect
from django.http import JsonResponse
# Create your views here.
from Guest.models import *
from Admin.models import *
from Recipient.models import *
from Donar.models import *
from datetime import date

def homepage(request):
    if 'did' in request.session:
        currentdate=date.today()
        eventcount=tbl_events.objects.filter(date__gt=currentdate).count()
        if eventcount>0:
            data=tbl_events.objects.filter(date__gt=currentdate)
            return render(request,"Donar/HomePage.html",{'data':data})
        else :
            return render(request,"Donar/HomePage.html")
    else:
        return redirect("Guest:login")

def myprofile(request):
    if 'did' in request.session:
        data=tbl_donar.objects.get(id=request.session["did"])
        return render(request,"Donar/MyProfile.html",{'data':data})
    else:
        return redirect("Guest:login")

def editprofile(request):
    if 'did' in request.session:
        data = tbl_donar.objects.get(id=request.session["did"])
        districts = tbl_district.objects.all()
        
        if request.method == "POST":
            address = request.POST.get('address')
            contact = request.POST.get('contact')

            # Validate contact contains only numbers
            if not contact.isdigit():
                return render(request, "Donar/EditProfile.html", {
                    'data': data,
                    'districts': districts,
                    'error': "Contact must contain only numbers"
                })

            # Validate address contains only letters and spaces
            if not all(char.isalpha() or char.isspace() for char in address):
                return render(request, "Donar/EditProfile.html", {
                    'data': data,
                    'districts': districts,
                    'error': "Address must contain only letters and spaces"
                })
            
            data.donar_name = request.POST.get('donar_name')
            data.contact = contact
            data.email = request.POST.get('email')
            data.address = address
            place_id = request.POST.get('place')
            if place_id:
                place = tbl_place.objects.get(id=place_id)
                data.place = place
            data.save()
            return redirect('Donar:editprofile')
        
        return render(request, "Donar/EditProfile.html", {
            'data': data,
            'districts': districts
        })
    else:
        return redirect("Guest:login")

def changepswd(request):
    if 'did' in request.session:
        if request.method=="POST":
            donarcount=tbl_donar.objects.filter(id=request.session["did"],password=request.POST.get('pswd')).count()
            if donarcount>0:
                if request.POST.get('new_pswd')==request.POST.get('c_pswd'):
                    donardata=tbl_donar.objects.get(id=request.session["did"])
                    donardata.password=request.POST.get('new_pswd')
                    donardata.save()
                    return redirect("Donar:homepage")
                else:
                    return render(request,"Donar/ChangePassword.html")
            else:
                return render(request,"Donar/ChangePassword.html")
        else:
            return render(request,"Donar/ChangePassword.html")
    else:
        return redirect("Guest:login")

def viewrequirements(request):
    if 'did' in request.session:
        requirementsdata=tbl_requirements.objects.filter(status=0)
        return render(request,"Donar/ViewRequirements.html",{'data':requirementsdata})
    else:
        return redirect("Guest:login")

def applyrequirements(request,aid):
    if 'did' in request.session:
        did=tbl_donar.objects.get(id=request.session["did"])
        rid=tbl_requirements.objects.get(id=aid)
        # Create application with initial status 0 (On Process)
        tbl_applyrequirements.objects.create(
            donar_id=did,
            requirements_id=rid,
            status=0
        )
        return redirect("Donar:viewrequirements")  
    else:
        return redirect("Guest:login")

def appliedrequirements(request):
    if 'did' in request.session:
        data=tbl_applyrequirements.objects.filter(donar_id=request.session["did"])
        return render(request,"Donar/AppliedRequirements.html",{'data':data})
    else:
        return redirect("Guest:login")

def chatuser(request, cid):
    if 'did' in request.session:
        chatobj = tbl_recipient.objects.get(id=cid)
        if request.method == "POST":
            cied = request.POST.get("cid")
            # print(cied)
            ciedobj = tbl_recipient.objects.get(id=cied)
            sobj = tbl_donar.objects.get(id=request.session["did"])
            content = request.POST.get("msg")
            # print(cied)
            # print(content)
            Chat.objects.create(
                from_donar=sobj, to_recipient=ciedobj, content=content, from_recipient=None, to_donar=None)
            return render(request, 'Donar/Chat.html', {"chatobj": chatobj})
        else:
            return render(request, 'Donar/Chat.html', {"chatobj": chatobj})
    else:
        return redirect("Guest:login")

def loadchatuser(request):
    if 'did' in request.session:
        cid = request.GET.get("cid")
        request.session["cid"] = cid
        cid1 = request.session["cid"]
        # print(cid1)
        # print(cid)
        shopobj = tbl_recipient.objects.get(id=cid)
        # print(userobj)
        sid = request.session["did"]
        # print(sid)
        suserobj = tbl_donar.objects.get(id=request.session["did"])
        # chatobj1 = Chat.objects.filter(Q(to_user=suserobj) | Q(
        #     from_user=suserobj), Q(to_shop=shopobj) | Q(from_shop=shopobj))
        # print(chatobj1)  # send message
        # print(chatobj2)  # recived msg
        chatobj = Chat.objects.raw(
            "select * from Recipient_chat c inner join Guest_tbl_donar u on (u.id=c.from_donar_id) or (u.id=c.to_donar_id) WHERE  c.from_recipient_id=%s or c.to_recipient_id=%s order by c.date", params=[(cid1), (cid1)])
        print(chatobj.query)
        return render(request, 'Donar/Load.html', {"obj": chatobj, "sid": sid, "shop": shopobj, "userobj": suserobj})
    else:
        return redirect("Guest:login")

def payment(request,rid):
    if 'did' in request.session:
        data=tbl_donar.objects.get(id=request.session["did"])
        pdetails=tbl_paymentrecord.objects.filter(donar_id=data)
        if request.method == "POST":
            r_id = tbl_requirements.objects.get(id=rid)
            d_id=tbl_donar.objects.get(id=request.session["did"])
            amt=request.POST.get('amount')
            tbl_paymentrecord.objects.create(requirements_id=r_id,donar_id=d_id,amount=amt)
            # tbl_applyrequirements.objects.create(requirements_id=r_id,donar_id=d_id,status=3)
            # reqdata=tbl_applyrequirements.objects.get(requirements_id=r_id)
            # reqdata.status=3
            # reqdata.save()
            return redirect('Donar:invoice')
        else:
            return render(request,"Donar/Payment.html")
    else:
        return redirect("Guest:login")
        
def invoice(request):
    if 'did' in request.session:
        currentdate=date.today()
        data=tbl_paymentrecord.objects.filter(donar_id=request.session["did"]).last()
        return render(request,"Donar/Invoice.html",{'data':data,'date':currentdate})
    else:
        return redirect("Guest:login")

def viewpayments(request):
    if 'did' in request.session:
        data=tbl_paymentrecord.objects.filter(donar_id=request.session["did"])
        return render(request,'Donar/ViewPayments.html', {'data':data})
    else:
        return redirect("Guest:login")

def viewevents(request,eid):
    if 'did' in request.session:
        data=tbl_events.objects.filter(id=eid)
        return render(request,'Donar/ViewEvents.html', {'data':data})
    else:
        return redirect("Guest:login")

def viewrecipients(request):
    if 'did' in request.session:
        districtdata=tbl_district.objects.all()
        placedata=tbl_place.objects.all()
        data=tbl_recipient.objects.all()
        return render(request,'Donar/ViewRecipients.html',{'data':data,'district':districtdata,'place':placedata})
    else:
        return redirect("Guest:login")

def ajaxrecipient(request):
    if request.GET.get("pid")!="":
        placedata=tbl_place.objects.get(id=request.GET.get('pid'))
        data=tbl_recipient.objects.filter(place=placedata)
        return render(request,"Donar/Ajaxrecipient.html",{'data':data})
    else:
        districtdata=tbl_district.objects.get(id=request.GET.get('did'))
        data=tbl_recipient.objects.filter(place__district=districtdata)
        return render(request,"Donar/Ajaxrecipient.html",{'data':data})

def bookappointment(request,rid):
    if 'did' in request.session:
        if request.method=="POST":
            did = tbl_donar.objects.get(id=request.session["did"])
            rid = tbl_recipient.objects.get(id=rid)
            appointment_date = request.POST.get('date')
            
            # Check if donor already has an appointment on this date
            existing_appointment = tbl_appointments.objects.filter(
                donar_id=did,
                date=appointment_date
            ).exists()
            
            if existing_appointment:
                error_message = "You already have an appointment scheduled for this date. Please choose a different date."
                return render(request, "Donar/BookAppointment.html", {'error': error_message})
            
            purps = request.POST.get('purpose')
            tim = request.POST.get('time')
            
            # Create new appointment if validation passes
            tbl_appointments.objects.create(
                donar_id=did,
                recipient_id=rid,
                date=appointment_date,
                purpose=purps,
                time=tim
            )
            success_message = "Appointment booked successfully!"
            return render(request, "Donar/BookAppointment.html", {'success': success_message})
        else:
            return render(request, "Donar/BookAppointment.html")
    else:
        return redirect("Guest:login")

def donaroffer(request,rid):
    if 'did' in request.session:
        if request.method=="POST":
            recipient=tbl_recipient.objects.get(id=rid)
            donar=tbl_donar.objects.get(id=request.session["did"])
            tbl_requirements.objects.create(recipient_id=recipient,
            details=request.POST.get('details'),requirement=request.POST.get('requirements'),for_date=request.POST.get('for_date'),status=4)
            requirement=tbl_requirements.objects.last()
            tbl_applyrequirements.objects.create(donar_id=donar,requirements_id=requirement,status=4)
            return render(request,"Donar/DonarOffer.html")
        else:
            return render(request,"Donar/DonarOffer.html")
    else:
        return redirect("Guest:login")

        
def viewappointments(request):
    if 'did' in request.session:
        data=tbl_appointments.objects.filter(donar_id=request.session["did"])
        return render(request,"Donar/ViewAppointments.html",{'data':data}) 
    else:
        return redirect("Guest:login") 
    
def cancelappointment(request,cid):
    data=tbl_appointments.objects.get(id=cid)
    data.status=2
    data.save()
    return redirect("Donar:viewappointments")

def acceptrequirements(request, rid):
    if 'did' in request.session:
        try:
            requirement = tbl_requirements.objects.get(id=rid)
            requirement.status = 1  # Update requirement status
            requirement.save()
            
            # Get donor instance
            donor = tbl_donar.objects.get(id=request.session["did"])
            
            # Get or create application
            application, created = tbl_applyrequirements.objects.get_or_create(
                donar_id=donor,
                requirements_id=requirement,
                defaults={'status': 1}  # Set initial status to 1 (Approved) if created
            )
            
            if not created:
                # If application already existed, update its status
                application.status = 1
                application.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Not authenticated'})

def complaint(request):
    if 'did' in request.session:
        if request.method=="POST":
            did=tbl_donar.objects.get(id=request.session["did"])
            tbl_complaint.objects.create(donar=did,title=request.POST.get('title'),content=request.POST.get('content'))
            return redirect("Donar:homepage")
        else:
            return render(request,"Donar/Complaint.html")
    else:
        return redirect("Guest:login") 

def reply(request):
    if 'did' in request.session:
        did=tbl_donar.objects.get(id=request.session["did"])
        data=tbl_complaint.objects.filter(donar=did)
        return render(request,"Donar/ViewReply.html",{'data':data})    
    else:
        return redirect("Guest:login") 

def feedback(request):
    if 'did' in request.session:
        if request.method=="POST":
            did=tbl_donar.objects.get(id=request.session["did"])
            tbl_feedback.objects.create(donar=did,content=request.POST.get('feedback'))
            return render(request,"Donar/feedback.html")
        else:
            return render(request,"Donar/feedback.html")
    else:
        return redirect("Guest:login") 

def logout(request):
    del request.session["did"]
    return redirect("Guest:home")
