from django.urls import path
from Recipient import views
# from Guest import views
app_name="Recipient"
urlpatterns = [
    path('home/',views.homepage,name="homepage"),
    path('myprofile/',views.myprofile,name="myprofile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepswd/',views.changepswd,name="changepswd"),
    path('requirements/',views.requirements,name="requirements"),
    path('editrequirement/<int:rid>',views.editrequirement,name="editrequirement"),
    path('deleterequirement/<int:rid>',views.deleterequirement,name="deleterequirement"),
    path('acceptrequirement/<int:aid>',views.acceptrequirement,name="acceptrequirement"),
    path('rejectrequirement/<int:rid>',views.rejectrequirement,name="rejectrequirement"),
    path('donaracceptance/',views.donaracceptance,name="donaracceptance"),
    path('confirmacceptance/<int:cid>',views.confirmacceptance,name="confirmacceptance"),
    path('rejectacceptance/<int:rid>',views.rejectacceptance,name="rejectacceptance"),
    path('acceptrejectlist/',views.acceptrejectlist,name="acceptrejectlist"),
    path('acceptconfirmlist/',views.acceptconfirmlist,name="acceptconfirmlist"),
    path('delivered/<int:did>',views.delivered,name="delivered"),
    path('deliveredlist/',views.deliveredlist,name="deliveredlist"),
    path('ajaxdonor/',views.ajaxdonor,name="ajaxdonor"),
    path('viewdonardetails/',views.viewdonardetails,name="viewdonardetails"),
    path('Chat/<int:cid>/', views.chatuser, name="Chat-user"),
    path('loadchat/', views.loadchatuser, name="load-chat"),
    path('viewpayments/',views.viewpayments,name="viewpayments"),
    path('events/',views.events,name="events"),
    path('editevent/<int:eid>',views.editevent,name="editevent"),
    path('deleteevent/<int:did>',views.deleteevent,name="deleteevent"),
    path('viewappointments/',views.viewappointments,name="viewappointments"),
    path('acceptappointment/<int:aid>/', views.acceptappointment, name="acceptappointment"),
    path('denyappointment/<int:did>/', views.denyappointment, name="denyappointment"),
    path('acceptedappointments/',views.acceptedappointments,name="acceptedappointments"),
    path('visitedappointment/<int:vid>/', views.visitedappointment, name="visitedappointment"),
    path('viewvisiters/',views.viewvisiters,name="viewvisiters"),
    path('complaint/', views.complaint, name="complaint"),
    path('reply/', views.reply, name="reply"),
    path('feedback/', views.feedback, name="feedback"),
    path('logout/', views.logout, name="logout"),

]