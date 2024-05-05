from django.urls import path
from . import views

urlpatterns = [
    path( 'admins/', views.admins, name='admins'),
    path( 'admins/login', views.login),
    path( 'admins/signUp', views.signUp),


]