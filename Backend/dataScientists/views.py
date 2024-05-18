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
from .models import DataScientist
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
from assessments.models import Assessment
import json
from django.utils import timezone
from django.db.utils import OperationalError
from utils.authenticators import generate_jwt_token
# import pandas lib as pd
import pandas as pd
import numpy as np
# Create your views here.
@api_view(['GET'])
def getDashboardData(request):
    try:
        dataFrame = pd.read_excel('cairouniversity_march_known_nooutliers.xlsx')
        print("hENAAAAA\n")
        print(dataFrame)
        #TODO:Uncomment trial & try again
        # # Convert DataFrame to JSON
        # # Loop over each column in the DataFrame
        # for col in dataFrame.columns:
        #     # Check if the column contains numeric data
        #     if np.issubdtype(dataFrame[col].dtype, np.number):
        #         # Replace out-of-range float values with a placeholder (np.nan)
        #         dataFrame[col] = dataFrame[col].replace([np.inf, -np.inf], np.nan)
        #         dataFrame[col] = dataFrame[col].astype(str)
        # json_data = dataFrame.to_json(orient='records')
        # Iterate over each row in the DataFrame
        json_objects = []
        for index, row in dataFrame.iterrows():
            # Convert the row to a dictionary
            row_dict = row.to_dict()
            # Append the dictionary to the list
            json_objects.append(row_dict)
        return Response({'success': True, 'data': json_objects})
        # return Response({'success': True,'message':'I\'m happy!'})
    except FileNotFoundError as e:
        # Return an error response if the file is not found
        return Response({'success': False, 'message': f'File not found: {e}'}, status=404)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)


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
        if DataScientist.objects.filter(email=email).exists():
            #compare password (methode 2)
            dataScientist=DataScientist.objects.get(email=email)
            print("My doctor object:\n",dataScientist)
            print("Database password:\n",dataScientist.password)
            print("User entered password:\n",password)

            print("Manual password checker:\n",type(password))
        
            # Check if user exists and password matches
            if dataScientist is None or not check_password(password, dataScientist.password):
                return Response({'success': False,'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                #TODO:set an expiration date
                token=generate_jwt_token(dataScientist.id)
                print("My token: ",token)
                return Response({'success': True,"id":dataScientist.id,"firstName":dataScientist.firstName,"lastName":dataScientist.lastName,'token': token,'message': 'Login successful'})
        else:
            # Email does not exist in the database
            return Response({'success': False, 'error': 'Email does not exist'}, status=400)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)


#===========================END BRAND NEW LOGIN=====================

@api_view(['POST'])
def forgotPassword(request):
    try:    
        # Get request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if both email and password are provided
        if email is None:
            return Response({'success': False, 'message': 'Please provide an email'}, status=400)
        if password is None:
            return Response({'success': False, 'message': 'Please provide a password'}, status=400)
        
        try:
            # Check if a Doctor object with the provided email exists
            dataScientist = DataScientist.objects.get(email=email)
            
            # Hash the new password
            hashed_password = make_password(password)
            
            # Update the password for the doctor object
            dataScientist.password = hashed_password
            
            # Save the doctor object to update the password in the database
            dataScientist.save()
            #TODO:Uncomment 
            # #send email to doctor
            # my_subject='Password notification for Baheya ALNM Website'
            # my_message='Your password is restored successfully. You can now login with your credentials.'
            # send_mail(
            #     subject=my_subject,
            #     message=my_message,
            #     recipient_list=[email],
            #     from_email=None,
            #     fail_silently=False)

            return Response({'success': True,'message': 'Password restored successfully.'})
        
        except ObjectDoesNotExist:
            # Handle the case where no Doctor object with the provided email exists
            return Response({'success': False, 'message': 'Email address not found.'}, status=404)
        
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)


#======================================================================================
