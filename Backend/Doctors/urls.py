from django.urls import path
from . import views

urlpatterns = [
    path( 'doctors/', views.doctors, name='doctors'),
    path( 'doctors/login', views.login),
    path( 'doctors/signUp', views.signUp),
    path( 'doctors/testToken', views.testToken),

]

#edited for signup

from django.urls import re_path 
from. import views
# urlpatterns = [
# re_path( 'login', views. login),
# re_path( 'signUp', views.signUp),
# re_path( 'testToken', views.testToken)
# ]