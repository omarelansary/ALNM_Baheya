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
from .models import headDoctor
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
from django.utils import timezone
from django.db.utils import OperationalError
from utils.authenticators import generate_jwt_token
from assessments.serializers import AssessmentSerializer
from collections import defaultdict 
import pandas as pd
from machineLearningModel.model import ALNM_Model
from headDoctors.serializers import HeadDoctorSerializer
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
#==========================GET HEAD DOCTORS============================================

@api_view(['GET'])
def getHeadDoctors(request):
    try:
        headDoctors=headDoctor.all()
        serializedHeadDoctors=HeadDoctorSerializer(headDoctors)
        return Response({'success': True,'headDoctors':serializedHeadDoctors})
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)

#======================================================================================
#=================================LOGIN AFTER CAPTCHA=====================================================
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
        doctor = headDoctor.objects.get(email=email)
        if check_password(password, doctor.password):
            # Generate JWT token
            token = generate_jwt_token(doctor.id)
            return Response({
                'success': True,
                'id': doctor.id,
                'firstName': doctor.firstName,
                'lastName': doctor.lastName,
                'token': token,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except headDoctor.DoesNotExist:
        return Response({'success': False, 'error': 'Email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

#=======================================================================================

@api_view(['POST'])
def delete(request):
    try: 
        doctor_id = request.data.get('doctor_id')

        # Check if both email and password are provided
        if doctor_id is None:
            return Response({'success': False, 'message': 'Doctor id is missing.'}, status=400)
        try:
            # Retrieve the doctor object based on the ID
            doctor = headDoctor.objects.get(id=doctor_id)
        except ObjectDoesNotExist:
            # Return failure response if doctor does not exist
            return Response({
                'success': False,
                'message': 'Doctor does not exist.'
            })

        # Proceed with deleting the doctor
        doctor.delete()

        return Response({'success': True, 'message': 'Doctor deleted successfully.'}, status=200)
        
    except OperationalError as e:
            # Return an error response for database errors
            return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
            # Return a generic error response for other exceptions
            return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)