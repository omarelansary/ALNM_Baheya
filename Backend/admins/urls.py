from django.urls import path
from . import views

urlpatterns = [
    path( 'admins/login', views.login),
    path( 'admins/signUp', views.signUp),
    path( 'admins/signUpDataScientists', views.signUpDataScientists),
    path( 'admins/getDoctors', views.getDoctors),   
    path( 'admins/getAssessments', views.getDoctors),   
    path( 'admins/getDoctors', views.getDoctors),   
    path( 'admins/getDataScientists', views.getDataScientists),  
    path( 'admins/signUpHeadDoctor', views.signUpHeadDoctor),   

    




]