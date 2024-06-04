from django.urls import path
from . import views

urlpatterns = [

    path( 'doctors/login', views.login),
    path( 'doctors/forgotPassword', views.forgotPassword),
    path( 'doctors/makeAssessment', views.makeAssessment),
    path( 'doctors/setGroundTruth', views.setGroundTruth), 
    path( 'doctors/getAssessmentsByDocId', views.getAssessmentsByDocId), 
    path( 'doctors/getStatusByMRN', views.getStatusByMRN), 
    path( 'doctors/getAssessmentsByStatus', views.getAssessmentsByStatus), 
    path( 'doctors/getAssessmentsCreationDate', views.getAssessmentsCreationDate), 
    path( 'doctors/delete', views.delete), 
    path( 'doctors/deleteAssessment', views.deleteAssessment), 
    path('doctors/captcha', views.get_captcha), 
    

    

    
    
    

    

]

