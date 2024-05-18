from django.urls import path
from . import views

urlpatterns = [
   
    path( 'dataScientists/login', views.login),
    path( 'dataScientists/forgotPassword', views.forgotPassword),
    path( 'dataScientists/getDashboardData', views.getDashboardData),
    path( 'dataScientists/export_assessments_to_excel', views.export_assessments_to_excel),
       

]

