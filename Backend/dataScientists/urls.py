from django.urls import path
from . import views

urlpatterns = [
    path( 'dataScientists/', views.dataScientists, name='dataScientists'),
    path( 'dataScientists/login', views.login),
    path( 'dataScientists/forgotPassword', views.forgotPassword),   

]

