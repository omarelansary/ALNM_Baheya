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
#======================================================================================
@api_view(['POST'])
def login(request):
    try:
        #TODO: return id , fisrat and lastname in the response -->DONE
        # Get request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if both email and password are provided
        if email is None or password is None:
            return Response({'success': False, 'message': 'Please provide both email and password'}, status=400)

        # Check if email already exists in the database
        if headDoctor.objects.filter(email=email).exists():
            #compare password (methode 2)
            head=headDoctor.objects.get(email=email)
            print("My doctor object:\n",head)
            print("Database password:\n",head.password)
            print("User entered password:\n",password)

            print("Manual password checker:\n",type(password))
        
            # Check if user exists and password matches
            if head is None or not check_password(password, head.password):
                return Response({'success': False,'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                #TODO:set an expiration date
                token=generate_jwt_token(head.id)
                print("My token: ",token)
                return Response({'success': True,"id":head.id,"firstName":head.firstName,"lastName":head.lastName,'token': token,'message': 'Login successful'})
        else:
            # Email does not exist in the database
            return Response({'success': False, 'error': 'Email does not exist'}, status=400)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)

