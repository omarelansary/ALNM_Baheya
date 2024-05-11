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
from doctors.models import Doctor
from .models import Admin
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.db.utils import OperationalError
from django.core.mail import send_mail

#Generate Token 
def generate_jwt_token(user_id):
    # Define payload (claims) for the JWT token
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
    }

    # Generate JWT token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token


# Create your views here.
#============Get Admins list==================================
@api_view(['GET'])
def admins(request):
    try:
        # Retrieve all records from the Admin model
        admins = Admin.objects.all()

        # Check if admins are found
        if admins:
            # Create a list to hold admin data
            admin_data = []
            # Iterate over the admins and populate the admin data list
            for admin in admins:
                admin_data.append({
                    'id': admin.id,
                    'email': admin.email,
                    'password':admin.password
                    # Add other fields as needed
                })
            # Return a success response with the admin data
            return Response({'success': True, 'data': admin_data})
        else:
            # Return an error response indicating no admins found
            return Response({'success': False, 'error': 'No admins found'}, status=404)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'error': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'error': f'An error occurred: {e}'}, status=500)
#===============End===========================================
#=========BRAND NEW SIGN UP========================================
#Steps:
#1-chek mail exists or new 
#2-create user
#3-send verification(fn) mail to user email 
#4-Return user not token

@api_view(['POST'])
def signUp(request):
    # Get request data
    firstName = request.data.get('firstName')
    lastName = request.data.get('lastName')
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if all required fields are provided
    if not firstName or not lastName or not email or not password:
        return Response({'success': False, 'message': 'Please provide all required fields'}, status=400)

    # Check if email already exists in the database
    if Doctor.objects.filter(email=email).exists():
        # Email already exists
        return Response({'success': False, 'message': 'Email already exists'}, status=400)
    else:
        try:
            #send email to doctor
            my_subject='Admin Verification for Baheya ALNM Website'
            # my_message=f'You can now login using the following credentials:\nEmail: {email}\nPassword: {password}'
            my_message=f'Please login with the following credentials:\nEmail: {email}\nPassword: {password}'
            send_mail(
                subject = my_subject,
                message = my_message,
                recipient_list= [email],
                from_email = None,
            fail_silently = False)
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

#=====BRAND NEW LOGIN FOR NEW MANUALLY DEFINED DOCTOR'S MODEL======

@api_view(['POST'])
def login(request):
    # Get request data
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if both email and password are provided
    if not email or not password:
        return Response({'success': False, 'message': 'Please provide both email and password'}, status=400)

    # Check if email already exists in the database
    if Admin.objects.filter(email=email).exists():
        #compare password (methode 2)
        admin=Admin.objects.get(email=email)
        print("My admin object:\n",admin)
        print("Database password:\n",admin.password)
        print("User entered password:\n",password)

        print("Manual password checker:\n",type(password))
     
        # Check if user exists and password matches
        if admin is None or password is not admin.password:
            return Response({'success': False,'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            #TODO:set an expiration date
            token=generate_jwt_token(admin.id)
            print("My token: ",token)
            return Response({'success': True,'token': token,'message': 'Login successful'})
    else:
        # Email does not exist in the database
        return Response({'success': False, 'error': 'Email does not exist'}, status=400)

#===========================END BRAND NEW LOGIN=====================