from django.urls import path
from . import views

urlpatterns = [

    path( 'headDoctors/login', views.login),
    path( 'headDoctors/getHeadDoctors', views.getHeadDoctors),

    
    
    
    
    

    

]

