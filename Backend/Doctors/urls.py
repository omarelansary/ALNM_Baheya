from django.urls import path
from . import views

urlpatterns = [
    path( 'doctors/', views.doctors, name='doctors'),
    path( 'doctors/login', views.login),
    path( 'doctors/forgotPassword', views.forgotPassword),
    path( 'doctors/makeAssessment', views.makeAssessment),

    

]

