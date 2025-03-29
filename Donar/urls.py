from django.urls import path
from Donar import views
app_name="Donar"
urlpatterns = [
    path('home/',views.homepage,name="homepage"),
    path('myprofile/',views.myprofile,name="myprofile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepswd/',views.changepswd,name="changepswd"),
    path('viewrequirements/',views.viewrequirements,name="viewrequirements"),
    path('applyrequirements/<int:aid>',views.applyrequirements,name="applyrequirements"),
    path('acceptrequirements/<int:rid>/',views.acceptrequirements,name="acceptrequirements"),
    path('appliedrequirements/',views.appliedrequirements,name="appliedrequirements"),
    path('Chat/<int:cid>/', views.chatuser, name="Chat-user"),
    path('loadchat/', views.loadchatuser, name="load-chat"), 
    path('payment/<int:rid>/', views.payment, name="payment"),   
    path('viewpayments/',views.viewpayments,name="viewpayments"), 
    path('viewevents/<int:eid>/',views.viewevents,name="viewevents"), 
    path('ajaxrecipient/',views.ajaxrecipient,name="ajaxrecipient"),
    path('viewrecipients/',views.viewrecipients,name="viewrecipients"), 
    path('bookappointment/<int:rid>/',views.bookappointment,name="bookappointment"), 
    path('viewappointments/',views.viewappointments,name="viewappointments"),
    path('cancelappointment/<int:cid>/', views.cancelappointment, name="cancelappointment"),
    path('donaroffer/<int:rid>/', views.donaroffer, name="donaroffer"),
    path('invoice/', views.invoice, name="invoice"),
    path('complaint/', views.complaint, name="complaint"),
    path('reply/', views.reply, name="reply"),
    path('feedback/', views.feedback, name="feedback"),
    path('logout/', views.logout, name="logout"),
]