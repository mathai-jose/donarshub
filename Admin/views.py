from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from Donar.models import *
from Recipient.models import *
from datetime import date
# Create your views here.
def homepage(request):
    if 'aid' in request.session:
        feedback=tbl_feedback.objects.raw('select * from Admin_tbl_feedback order by date desc limit 3 ')
        event=tbl_events.objects.raw('select * from Recipient_tbl_events where status=1 order by date desc limit 3 ')
        paycount=tbl_paymentrecord.objects.filter().count()
        req=tbl_applyrequirements.objects.filter().count()
        count=paycount+req
        donarcount=tbl_donar.objects.filter().count()
        eventcount=tbl_events.objects.filter().count()
        appointmentcount=tbl_appointments.objects.filter().count()
        recipientcount=tbl_recipient.objects.filter().count()
        requirementcount=tbl_requirements.objects.filter().count()
        districtdata=tbl_district.objects.all()
        return render(request,"Admin/HomePage.html",{'data1':feedback,'data2':event,'donation':count,'donar':donarcount,'recipient':recipientcount,'requirement':requirementcount,'appointment':appointmentcount,'event':eventcount,'district':districtdata})
    else:
        return redirect("Guest:login")
def district(request):
    if 'aid' in request.session:
        districtdata=tbl_district.objects.all()
        if request.method=="POST":
            tbl_district.objects.create(district_name=request.POST.get('district'))
            return render(request,"Admin/District.html",{'district':districtdata})
        else:
            return render(request,"Admin/District.html",{'district':districtdata})
    else:
        return redirect("Guest:login")

def deletedistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect("Admin:dist")

def editdistrict(request,did):
    data=tbl_district.objects.get(id=did)
    if request.method=="POST":
        data.district_name=request.POST.get('district')
        data.save()
        return redirect("Admin:dist")
    else:
        return render(request,"Admin/District.html",{'data':data})
    
def category(request):
    if 'aid' in request.session:
        categorydata=tbl_category.objects.all()
        if request.method=="POST":
            tbl_category.objects.create(category_name=request.POST.get('category'))
            return render(request,"Admin/Category.html",{'category':categorydata})
        else:
            return render(request,"Admin/Category.html",{'category':categorydata})
    else:
        return redirect("Guest:login")        

def deletecategory(request,cid):
    tbl_category.objects.get(id=cid).delete()
    return redirect("Admin:cat")
def editcategory(request,cid):
    data=tbl_category.objects.get(id=cid)
    if request.method=="POST":
        data.category_name=request.POST.get('category')
        data.save()
        return redirect("Admin:cat")
    else:
        return render(request,"Admin/Category.html",{'data':data})

def brand(request):
    if 'aid' in request.session:
        branddata=tbl_brand.objects.all()
        if request.method=="POST":
            tbl_brand.objects.create(brand_name=request.POST.get('brand'))
            return render(request,"Admin/Brand.html",{'brand':branddata})
        else:
            return render(request,"Admin/Brand.html",{'brand':branddata})
    else:
        return redirect("Guest:login")

def deletebrand(request,bid):
    tbl_brand.objects.get(id=bid).delete()
    return redirect("Admin:brand")

def place(request):
    if 'aid' in request.session:
        districtdata=tbl_district.objects.all()
        placedata=tbl_place.objects.all()
        if request.method=="POST":
            dis=tbl_district.objects.get(id=request.POST.get('district'))
            tbl_place.objects.create(place_name=request.POST.get('place'),district=dis)
            return render(request,"Admin/Place.html",{'district':districtdata,'place':placedata})
        else:
            return render(request,"Admin/Place.html",{'district':districtdata,'place':placedata})
    else:
        return redirect("Guest:login")

def deleteplace(request,pid):
    tbl_place.objects.get(id=pid).delete()
    return redirect("Admin:place")

def subcategory(request):
    if 'aid' in request.session:
        categorydata=tbl_category.objects.all()
        subcategorydata=tbl_subcategory.objects.all()
        if request.method=="POST":
            cat=tbl_category.objects.get(id=request.POST.get('category'))
            tbl_subcategory.objects.create(subcategory_name=request.POST.get('subcategory'),category=cat)
            return render(request,"Admin/Subcategory.html",{'category':categorydata,'subcategory':subcategorydata})
        else:
            return render(request,"Admin/Subcategory.html",{'category':categorydata,'subcategory':subcategorydata})
    else:
        return redirect("Guest:login")

def deletesubcategory(request,sid):
    tbl_subcategory.objects.get(id=sid).delete()
    return redirect("Admin:subcategory")

def newlist(request):
    if 'aid' in request.session:
        data=tbl_donar.objects.filter(status=0)
        return render(request,"Admin/Newlist.html",{'data':data})
    else:
        return redirect("Guest:login")

def rejectedlist(request):
    if 'aid' in request.session:
        data=tbl_donar.objects.filter(status=2)
        return render(request,"Admin/Rejectedlist.html",{'data':data})
    else:
        return redirect("Guest:login")

def acceptedlist(request):
    if 'aid' in request.session:
        data=tbl_donar.objects.filter(status=1)
        return render(request,"Admin/Acceptedlist.html",{'data':data})
    else:
        return redirect("Guest:login")

def acceptdonar(request,aid):
    data=tbl_donar.objects.get(id=aid)
    data.status=1
    data.save()
    return redirect("Admin:newlist")

def rejectdonar(request,rid):
    data=tbl_donar.objects.get(id=rid)
    data.status=2
    data.save()
    return redirect("Admin:newlist")

def recipientlist(request):
    if 'aid' in request.session:
        data=tbl_recipient.objects.all()
        return render(request,"Admin/Recipientlist.html",{'data':data})
    else:
        return redirect("Guest:login")

def adminreg(request):
    data=tbl_adminlogin.objects.all()
    if request.method == "POST":
        aname=request.POST.get('a_name')
        aemail=request.POST.get('email')
        apassword=request.POST.get('password')
        tbl_adminlogin.objects.create(name=aname,email=aemail,password=apassword)
        return render(request,"Admin/AdminRegistration.html",{'Data':data})
    else:
        return render(request,"Admin/AdminRegistration.html",{'Data':data})

def deleteadmin(request,aid):
    tbl_adminlogin.objects.get(id=aid).delete()
    return redirect("Admin:adminreg")

def editadmin(request,aid):
    data=tbl_adminlogin.objects.get(id=aid)
    if request.method=="POST":
        data.name=request.POST.get('a_name')
        data.email=request.POST.get('email')
        data.password=request.POST.get('password')
        data.save()
        return redirect("Admin:adminreg")
    else:
        return render(request,"Admin/AdminRegistration.html",{'data':data})

def payreport(request):
    if 'aid' in request.session:
        if request.method == "POST":
            f_date=request.POST.get('f_date')
            t_date=request.POST.get('t_date')
            if f_date!="" and t_date!="":
                data=tbl_paymentrecord.objects.filter(date__gt=f_date,date__lte=t_date)
                return  render(request,"Admin/PaymentReport.html",{'Data':data})
            elif f_date!="":
                data=tbl_paymentrecord.objects.filter(date__gte=f_date)
                return  render(request,"Admin/PaymentReport.html",{'Data':data})
            else:
                data=tbl_paymentrecord.objects.filter(date__lte=t_date)
                return  render(request,"Admin/PaymentReport.html",{'Data':data})
        else:
            return  render(request,"Admin/PaymentReport.html")
    else:
        return redirect("Guest:login")

def areqreport(request):
    if 'aid' in request.session:
        if request.method == "POST":
            f_date=request.POST.get('f_date')
            t_date=request.POST.get('t_date')
            if f_date!="" and t_date!="":
                data=tbl_applyrequirements.objects.filter(requirements_id__date_of_post__gt=f_date,requirements_id__date_of_post__lte=t_date)
                return  render(request,"Admin/AppliedRequirementReport.html",{'Data':data})
            elif f_date!="":
                data=tbl_applyrequirements.objects.filter(requirements_id__date_of_post__gte=f_date)
                return  render(request,"Admin/AppliedRequirementReport.html",{'Data':data})
            else:
                data=tbl_applyrequirements.objects.filter(requirements_id__date_of_post__lte=t_date)
                return  render(request,"Admin/AppliedRequirementReport.html",{'Data':data})
        else:
            return  render(request,"Admin/AppliedRequirementReport.html")
    else:
        return redirect("Guest:login")

def reqreport(request):
    if 'aid' in request.session:
        if request.method == "POST":
            f_date=request.POST.get('f_date')
            t_date=request.POST.get('t_date')
            if f_date!="" and t_date!="":
                data=tbl_requirements.objects.filter(date_of_post__gt=f_date,date_of_post__lte=t_date)
                return  render(request,"Admin/RequirementReport.html",{'Data':data})
            elif f_date!="":
                data=tbl_requirements.objects.filter(date_of_post__gte=f_date)
                return  render(request,"Admin/RequirementReport.html",{'Data':data})
            else:
                data=tbl_requirements.objects.filter(date_of_post__lte=t_date)
                return  render(request,"Admin/RequirementReport.html",{'Data':data})
        else:
            return  render(request,"Admin/RequirementReport.html")
    else:
        return redirect("Guest:login")

def feedback(request):
    if 'aid' in request.session:
        data=tbl_feedback.objects.all()
        return render(request,"Admin/ViewFeedback.html",{'data':data})
    else:
        return redirect("Guest:login")

def complaint(request):
    if 'aid' in request.session:      
            data=tbl_complaint.objects.filter(status=0)
            return render(request,"Admin/ViewComplaint.html",{'data':data})      
    else:
        return redirect("Guest:login")
def reply(request,rpid):
    if 'aid' in request.session:  
        data=tbl_complaint.objects.get(id=rpid)
        if request.method == "POST":
            currentdate=date.today()
            data.reply=request.POST.get('reply')
            data.reply_date=currentdate
            data.status=1
            data.save()
            return render(request,"Admin/Reply.html",{'data':data})
        else:
            return render(request,"Admin/Reply.html",{'data':data})
    else:
        return redirect("Guest:login")
        
def logout(request):
    del request.session["aid"]
    return redirect("Guest:home")

def profile(request):
    if 'aid' in request.session: 
        aid=request.session["aid"]
        data=tbl_adminlogin.objects.get(id=aid) 
        return render(request,"Admin/AdminProfile.html",{'data':data})
    else:
        return redirect("Guest:login")