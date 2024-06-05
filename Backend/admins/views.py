# #
import smtplib
import ssl
# request = "https://nd-123-456-789.p2pify.com/901c7d18b72538fd3324248e1234" urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
# #

from django.shortcuts import render
from django.http import HttpResponse
#edited
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status 
#Allows us to fetch and create users and tokens from our database
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from django. shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.db.utils import OperationalError
from django.core.mail import send_mail
from utils.authenticators import generate_jwt_token
from rest_framework.renderers import JSONRenderer
from doctors.serializers import DoctorSerializer
from dataScientists.serializers import DataScientistSerializer
from assessments.serializers import AssessmentSerializer
#Import your models here
from .models import Admin
from doctors.models import Doctor
from dataScientists.models import DataScientist
from assessments.models import Assessment
from headDoctors.models import headDoctor
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

#=========BRAND NEW SIGN UP========================================
#Steps:
#1-chek mail exists or new 
#2-create user
#3-send verification(fn) mail to user email 
#4-Return user not token

@api_view(['POST'])
def signUp(request):
    try:
        # Get request data
        firstName = request.data.get('firstName')
        lastName = request.data.get('lastName')
        email = request.data.get('email')
        password = request.data.get('password')
        # captcha_key = request.data.get('captcha_key')
        # captcha_value = request.data.get('captcha_value')

        # Check if all required fields are provided
        if not firstName or not lastName or not email or not password:
            return Response({'success': False, 'message': 'Please provide all required fields'}, status=400)

        # # Validate captcha
        # if not validate_captcha(captcha_key, captcha_value):
        #     return Response({'success': False, 'message': 'Invalid captcha'}, status=400)


        # Check if email already exists in the database
        if Doctor.objects.filter(email=email).exists():
            # Email already exists
            return Response({'success': False, 'message': 'Email already exists'}, status=400)
        else:
            try:
                #TODO: Uncomment
                # #send email to doctor
                # my_subject='Admin Verification for Baheya ALNM Website'
                # # my_message=f'You can now login using the following credentials:\nEmail: {email}\nPassword: {password}'
                # my_message=f'Please login with the following credentials:\nEmail: {email}\nPassword: {password}'
                # send_mail(
                #     subject = my_subject,
                #     message = my_message,
                #     recipient_list= [email],
                #     from_email = None,
                # fail_silently = False)
                # Hash the password using bcrypt
                # hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # Hash the password using Django's default hashing algorithm
                hashedPassword = make_password(password)
                # # Convert the hashed password to a string
                # hashedPassword_str = hashedPassword.decode('utf-8')

                # Create a new Doctor instance
                doctor = Doctor.objects.create(
                    firstName=firstName,
                    lastName=lastName,
                    email=email,
                    password=hashedPassword
                )
                

                # Return success response with doctor details
                return Response({'success': True, 'doctor': {'id': doctor.id, 'firstName': doctor.firstName, 'lastName': doctor.lastName, 'email': doctor.email,'password':doctor.password}, 'message': 'Doctor created successfully'})
            except Exception as e:
                return Response({'success': False, 'message': str(e)}, status=500)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)

#===============================LOGIN AFTER CAPTCHA=====================
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    captcha_key = request.data.get('captcha_key')
    captcha_response = request.data.get('captcha_response')

    # Check if email, password, and captcha fields are provided
    if not email or not password or not captcha_key or not captcha_response:
        return Response({'success': False, 'error': 'Please provide email, password, captcha key, and captcha response'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify CAPTCHA
    if not CaptchaStore.objects.filter(hashkey=captcha_key).exists():
        return Response({'success': False, 'error': 'Invalid captcha key'}, status=status.HTTP_400_BAD_REQUEST)
    
    captcha = CaptchaStore.objects.get(hashkey=captcha_key)
    if not captcha.response.lower() == captcha_response.lower():
        print("captcha.response:\n",captcha.response)
        print("captcha_response:\n",captcha_response)
        
        return Response({'success': False, 'error': 'Invalid captcha response'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if email exists in the database
    try:
        admin = Admin.objects.get(email=email)
        if check_password(password, admin.password):
            # Generate JWT token
            token = generate_jwt_token(admin.id)
            return Response({
                'success': True,
                'id': admin.id,
                'firstName': admin.firstName,
                'lastName': admin.lastName,
                'token': token,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Admin.DoesNotExist:
        return Response({'success': False, 'error': 'Email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

#===========================END BRAND NEW LOGIN=====================

#============================SIGN UP DATA SCIENTISTS===================
@api_view(['POST'])
def signUpDataScientists(request):
    try:
        # Get request data
        firstName = request.data.get('firstName')
        lastName = request.data.get('lastName')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if all required fields are provided
        if not firstName or not lastName or not email or not password:
            return Response({'success': False, 'message': 'Please provide all required fields'}, status=400)

        # Check if email already exists in the database
        if DataScientist.objects.filter(email=email).exists():
            # Email already exists
            return Response({'success': False, 'message': 'Email already exists'}, status=400)
        else:
            try:
                #TODO: Uncomment
                # #send email to doctor
                # my_subject='Admin Verification for Baheya ALNM Website'
                # # my_message=f'You can now login using the following credentials:\nEmail: {email}\nPassword: {password}'
                # my_message=f'Please login with the following credentials:\nEmail: {email}\nPassword: {password}'
                # send_mail(
                #     subject = my_subject,
                #     message = my_message,
                #     recipient_list= [email],
                #     from_email = None,
                # fail_silently = False)
                # Hash the password using bcrypt
                # hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # Hash the password using Django's default hashing algorithm
                hashedPassword = make_password(password)
                # # Convert the hashed password to a string
                # hashedPassword_str = hashedPassword.decode('utf-8')

                # Create a new Doctor instance
                dataScientist = DataScientist.objects.create(
                    firstName=firstName,
                    lastName=lastName,
                    email=email,
                    password=hashedPassword
                )
                

                # Return success response with doctor details
                return Response({'success': True, 'dataScientist': {'id': dataScientist.id, 'firstName': dataScientist.firstName, 'lastName': dataScientist.lastName, 'email': dataScientist.email,'password':dataScientist.password}, 'message': 'Data Scientist created successfully'})
            except Exception as e:
                return Response({'success': False, 'message': str(e)}, status=500)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)
#====================SIGNUP FOR HEAD OF DOCTORS==================================

@api_view(['POST'])
def signUpHeadDoctor(request):
    try:
        # Get request data
        firstName = request.data.get('firstName')
        lastName = request.data.get('lastName')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if all required fields are provided
        if not firstName or not lastName or not email or not password:
            return Response({'success': False, 'message': 'Please provide all required fields'}, status=400)

        # Check if email already exists in the database
        if headDoctor.objects.filter(email=email).exists():
            # Email already exists
            return Response({'success': False, 'message': 'Email already exists'}, status=400)
        else:
            try:
                #TODO: Uncomment
                # #send email to doctor
                # my_subject='Admin Verification for Baheya ALNM Website'
                # # my_message=f'You can now login using the following credentials:\nEmail: {email}\nPassword: {password}'
                # my_message=f'Please login with the following credentials:\nEmail: {email}\nPassword: {password}'
                # send_mail(
                #     subject = my_subject,
                #     message = my_message,
                #     recipient_list= [email],
                #     from_email = None,
                # fail_silently = False)
                # Hash the password using bcrypt
                # hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                # Hash the password using Django's default hashing algorithm
                hashedPassword = make_password(password)
                # # Convert the hashed password to a string
                # hashedPassword_str = hashedPassword.decode('utf-8')

                # Create a new Doctor instance
                head = headDoctor.objects.create(
                    firstName=firstName,
                    lastName=lastName,
                    email=email,
                    password=hashedPassword
                )
                

                # Return success response with doctor details
                return Response({'success': True, 'headDoctor': {'id': head.id, 'firstName': head.firstName, 'lastName': head.lastName, 'email': head.email,'password':head.password}, 'message': 'Head of Doctors created successfully'})
            except Exception as e:
                return Response({'success': False, 'message': str(e)}, status=500)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)



#======================================================================

#====================================GETTERS=======================================
@api_view(['GET'])
def getDoctors(request):
    try:
        doctors = Doctor.objects.all()

        serializedDoctors = DoctorSerializer(doctors, many=True)


        return Response({'success':True,'doctors':serializedDoctors.data})
    except OperationalError as e:
        # Return an error response for database errors 
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)
               
#=============================================================================

@api_view(['GET'])
def getDataScientists(request):
    try:
        DataScientists = DataScientist.objects.all()

        serializedDataScientists = DataScientistSerializer(DataScientists, many=True)


        return Response({'success':True,'dataScientists':serializedDataScientists.data})
    except OperationalError as e:
        # Return an error response for database errors 
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)
               
#=============================================================================