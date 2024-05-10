from django.shortcuts import render
from django.http import HttpResponse
#edited
from rest_framework.decorators import api_view 
from rest_framework.response import Response
# from serializers import UserSerializer 
from doctors.serializers import UserSerializer
from rest_framework import status 
#Allows us to fetch and create users and tokens from our database
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from django. shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Doctor
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from patients.models import Patient
from assessments.models import Assessment
import json

def generate_jwt_token(user_id):
    # Define payload (claims) for the JWT token
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
    }

    # Generate JWT token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token

@api_view( ['GET'])
def doctors(request):
    return Response({"message":"This is the doctor's Api"})

@api_view(['POST'])
def forgotPassword(request):
    # Get request data
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if both email and password are provided
    if not email:
        return Response({'success': False, 'message': 'Please provide an email'}, status=400)
    if not password:
        return Response({'success': False, 'message': 'Please provide a password'}, status=400)
    
    try:
        # Check if a Doctor object with the provided email exists
        doctor = Doctor.objects.get(email=email)
        
        # Hash the new password
        hashed_password = make_password(password)
        
        # Update the password for the doctor object
        doctor.password = hashed_password
        
        # Save the doctor object to update the password in the database
        doctor.save()

        #send email to doctor
        my_subject='Password notification for Baheya ALNM Website'
        my_message='Your password is restored successfully. You can now login with your credentials.'
        send_mail(
            subject=my_subject,
            message=my_message,
            recipient_list=[email],
            from_email=None,
            fail_silently=False)

        return Response({'success': True,'message': 'Password restored successfully.'})
    
    except ObjectDoesNotExist:
        # Handle the case where no Doctor object with the provided email exists
        return Response({'success': False, 'message': 'Email address not found.'}, status=404)
    
    except Exception as e:
        # Handle unexpected exceptions
        return Response({'success': False, 'message': 'An unexpected error occurred.'}, status=500)


#======================================================================================
@api_view(['POST'])
def login(request):
    # Get request data
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if both email and password are provided
    if not email or not password:
        return Response({'success': False, 'message': 'Please provide both email and password'}, status=400)

    # Check if email already exists in the database
    if Doctor.objects.filter(email=email).exists():
        #compare password (methode 2)
        doctor=Doctor.objects.get(email=email)
        print("My doctor object:\n",doctor)
        print("Database password:\n",doctor.password)
        print("User entered password:\n",password)

        print("Manual password checker:\n",type(password))
     
        # Check if user exists and password matches
        if doctor is None or not check_password(password, doctor.password):
            return Response({'success': False,'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            #TODO:set an expiration date
            token=generate_jwt_token(doctor.id)
            print("My token: ",token)
            return Response({'success': True,'token': token,'message': 'Login successful'})
    else:
        # Email does not exist in the database
        return Response({'success': False, 'error': 'Email does not exist'}, status=400)

#===========================END BRAND NEW LOGIN=====================
#===========================Risk Assessment View====================
'''
This function takes the doctor id and patients MRN along with other medical info
It allows multiple doctors to insert patients data but ONLY once each

'''

# @api_view(['POST'])
# def insertAndRetrievePatientInfo(request):
    
#     # Extract doctor_id and medical_info from the request
#     doctor_id = request.data.get('doctor_id')
#     MRN = request.data.get('medical_info').get('MRN')

#     # Check if doctor_id and MRN are provided
#     if not doctor_id or not MRN:
#         return Response({
#             'success': False,
#             'message': 'Doctor ID or MRN is missing.'
#         })
#     # Check if medical_info is provided
#     medical_info = request.data.get('medical_info')
#     if not medical_info:
#         return Response({
#             'success': False,
#             'message': 'Medical info is missing.'
#         })
    
#     try:
#         # Retrieve the doctor object based on the ID
#         doctor = Doctor.objects.get(id=doctor_id)
#     except ObjectDoesNotExist:
#         # Return failure response if doctor does not exist
#         return Response({
#             'success': False,
#             'message': 'Doctor does not exist.'
#         })
    
#     try:
#         patient = Patient.objects.get(MRN=MRN)
#     except ObjectDoesNotExist:
#         patient = Patient.objects.create()

#     # Check if the doctor is already associated with the patient
#     if patient.objects.filter(doctors__id=doctor_id).exists():
#         return Response({
#             'success': False,
#             'message': 'Doctor already created this patient before.'
#         })


    


#     # No need to parse medical_info as JSON since it's already a dictionary
#     # try:
#     #     # Parse medical_info as JSON
#     #     medical_info = json.loads(medical_info)
#     # except json.JSONDecodeError:
#     #     # Return failure response if medical_info is not valid JSON
#     #     return Response({
#     #         'success': False,
#     #         'message': 'Invalid medical info format.'
#     #     })


#     # Use the set_medical_info method to set medical info for the patient
#     patient.set_medical_info(
#         MRN=medical_info.get('MRN'),
#         patient_first_bmi=medical_info.get('patient_first_bmi'),
#         patient_age=medical_info.get('patient_age'),
#         patient_size_cm=medical_info.get('patient_size_cm'),
#         patient_ki67=medical_info.get('patient_ki67'),
#         patient_family_history=medical_info.get('patient_family_history'),
#         patient_menopausal_state=medical_info.get('patient_menopausal_state'),
#         patient_t=medical_info.get('patient_t'),
#         patient_n=medical_info.get('patient_n'),
#         patient_laterality=medical_info.get('patient_laterality'),
#         patient_unilateral_bilateral=medical_info.get('patient_unilateral_bilateral'),
#         patient_site=medical_info.get('patient_site'),
#         patient_tumor_type=medical_info.get('patient_tumor_type'),
#         patient_grade=medical_info.get('patient_grade')
#     )


#     # Add the doctor to the patient's doctors
#     patient.doctors.add(doctor)

#     # Save the patient object
#     patient.save()

#     # Return the patient object in the response
#     return Response({
#         'success': True,
#         'id': patient.id,
#         'medical_info': patient.medical_info,
#         'doctors': [doc.id for doc in patient.doctors.all()]
#     })
#####################################
@api_view(['POST'])
def makeAssessment(request):
    
    # Extract doctor_id and medical_info from the request
    doctor_id = request.data.get('doctor_id')
    medical_info = request.data.get('medical_info')
    MRN=request.data.get('MRN')
    # Check if doctor_id and medical_info are provided
    if not doctor_id or not medical_info or not MRN:
        return Response({
            'success': False,
            'message': 'Doctor ID, medical info or MRN is missing.'
        })

    try:
        # Retrieve the doctor object based on the ID
        doctor = Doctor.objects.get(id=doctor_id)
    except ObjectDoesNotExist:
        # Return failure response if doctor does not exist
        return Response({
            'success': False,
            'message': 'Doctor does not exist.'
        })
    
    try:
        # Attempt to retrieve the assessment object based on MRN
        assessment = Assessment.objects.get(MRN=MRN)
    except Assessment.DoesNotExist:
        # If the assessment doesn't exist, create a new one
        assessment = Assessment.objects.create(MRN=MRN)

    # Check if the doctor is already associated with the assessment
    if assessment.doctors.filter(id=doctor_id).exists():
        return Response({
            'success': False,
            'message': 'Doctor already associated with this assessment.'
        })

    # Use the method to set medical info for the assessment
    assessment.set_medical_info(
        MRN=MRN,
        patient_first_bmi=medical_info.get('patient_first_bmi'),
        patient_age=medical_info.get('patient_age'),
        patient_size_cm=medical_info.get('patient_size_cm'),
        patient_ki67=medical_info.get('patient_ki67'),
        patient_family_history=medical_info.get('patient_family_history'),
        patient_menopausal_state=medical_info.get('patient_menopausal_state'),
        patient_t=medical_info.get('patient_t'),
        patient_n=medical_info.get('patient_n'),
        patient_laterality=medical_info.get('patient_laterality'),
        patient_unilateral_bilateral=medical_info.get('patient_unilateral_bilateral'),
        patient_site=medical_info.get('patient_site'),
        patient_tumor_type=medical_info.get('patient_tumor_type'),
        patient_grade=medical_info.get('patient_grade'),
        dm_result=medical_info.get('dm_result'),
        htn_result=medical_info.get('htn_result'),
        vte_result=medical_info.get('vte_result'),
        cvd_result=medical_info.get('cvd_result'),
        lymphovascular_invasion_result=medical_info.get('lymphovascular_invasion_result'),
        er_result=medical_info.get('er_result'),
        pr_result=medical_info.get('pr_result'),
        her2_result=medical_info.get('her2_result')
    )

    # Add the doctor to the assessment's doctors
    assessment.doctors.add(doctor)

    # Save the assessment object
    assessment.save()

    # Return the assessment object in the response
    return Response({
        'success': True,
        'id': assessment.id,
        'medical_info': assessment.medical_info,
        'doctors': [doc.id for doc in assessment.doctors.all()]
    })


#===================================================================

#=========================================================================
# @api_view( ['POST'])
# def login (request) :
#   user = get_object_or_404(User, username=request.data ['username'])
#   if not user. check_password (request.data[ 'password']):
#     return Response({"detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
#   token, created = Token.objects.get_or_create(user=user)
#   serializer = UserSerializer (instance=user)
#   return Response({"token": token.key, "user": serializer.data})

#New login for both data and token authentication
# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     # Authenticate the user using username and password
#     user = authenticate(username=username, password=password)

#     if user:
#         # If user is authenticated, generate or retrieve a token
#         token, created = Token.objects.get_or_create(user=user)
        
#         # Serialize the user object to include user data in the response
#         serializer = UserSerializer(instance=user)
        
#         # Return the token and user data in the response
#         return Response({"token": token.key, "user": serializer.data})
#     else:
#         # If authentication fails, return a 404 Not Found response
#         return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
# #===================================================================================

# @api_view( ['POST'])
# def signUp (request) :
#   #Get serializer instance based on the data passed in our request
#   serializer = UserSerializer(data=request.data)
#   #Check if data valid (username,password & email recieved)
#   if serializer.is_valid():
#     serializer.save()
#     #Retrieve user by username
#     user = User.objects.get (username=request. data ['username'] )
#     #Save password in a hashed(encoded) format for security reasons
#     user.set_password (request.data ['password'])
#     user.save()
#     #Generate token for frontend
#     token = Token.objects.create(user=user)

#     #Return user token and data
#     return Response({"token": token.key, "user": serializer.data})
#   return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
