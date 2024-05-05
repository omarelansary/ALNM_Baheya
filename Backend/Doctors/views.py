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

#=========BRAND NEW SIGN UP========================================
#Steps:
#1-chek mail exists or new 
#2-create user
#3-send verification(fn) mail to user email 
#4-Return user not token

@api_view(['POST'])
def signUp(request):
    # Get request data
    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if all required fields are provided
    if not first_name or not last_name or not email or not password:
        return Response({'success': False, 'message': 'Please provide all required fields'}, status=400)

    # Check if email already exists in the database
    if Doctor.objects.filter(email=email).exists():
        # Email already exists
        return Response({'success': False, 'message': 'Email already exists'}, status=400)
    else:
        # # Hash the password using bcrypt
        # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Hash the password using Django's default hashing algorithm
        hashed_password = make_password(password)
        # # Convert the hashed password to a string
        # hashed_password_str = hashed_password.decode('utf-8')

        # Create a new Doctor instance
        doctor = Doctor.objects.create(
            firstName=first_name,
            lastName=last_name,
            email=email,
            password=hashed_password
        )
        # Return success response with doctor details
        return Response({'success': True, 'doctor': {'id': doctor.id, 'firstName': doctor.firstName, 'lastName': doctor.lastName, 'email': doctor.email,'password':doctor.password}, 'message': 'Doctor created successfully'})

#=====BRAND NEW LOGIN FOR NEW MANUALLY DEFINED DOCTOR'S MODEL======

#================================
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
        print("Manual password checker:")
        print(type(password))
        print("Password matching check: ",check_password(doctor.password,password))
        # Email exists, proceed with authentication
        user = authenticate(email=email, password=password)
        

        
        

        token=generate_jwt_token(doctor.id)
        print("My token: ",token)

        if user is not None:
            
            # # Serialize the user object to include user data in the response
            # serializer = UserSerializer(instance=user)
            # Authentication successful
            
            # Here you can perform any additional tasks you need
            return Response({'success': True,'token': token,'message': 'Login successful'})
            
        else:
            # Authentication failed
            return Response({'success': False ,'message': 'Invalid credentials'}, status=400)
    else:
        # Email does not exist in the database
        return Response({'success': False, 'message': 'Email does not exist'}, status=400)

#===========================END BRAND NEW LOGIN=====================

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


@api_view( ['POST'])
def testToken(request):
  return Response ({"message":"This is the doctor's testtoken Api"})