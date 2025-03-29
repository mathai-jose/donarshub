from django.urls import path
from Guest import views
app_name="Guest"
urlpatterns = [
    path('donarregistration/',views.donarregistration,name="donarregistration"),
    path('recipientregistration/',views.recipientregistration,name="recipientregistration"),   
    path('ajax_place/',views.ajax_place,name="Ajax_Place"),
    path('login/',views.login,name="login"),
    path('fpass/', views.ForgetPassword,name="forpass"),
    path('otpver/', views.OtpVerification,name="verification"),
    path('create/', views.CreateNewPass,name="create"),
    path('', views.home,name="home"),
    path('ajaxemail/', views.ajaxemail,name="ajaxemail"),
    path('get_places/', views.get_places, name='get_places'),
]