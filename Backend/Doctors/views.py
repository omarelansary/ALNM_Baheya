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


@api_view( ['GET'])
def doctors(request):
    return Response({"message":"This is the doctor's Api"})

# @api_view( ['POST'])
# def login (request) :
#   user = get_object_or_404(User, username=request.data ['username'])
#   if not user. check_password (request.data[ 'password']):
#     return Response({"detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
#   token, created = Token.objects.get_or_create(user=user)
#   serializer = UserSerializer (instance=user)
#   return Response({"token": token.key, "user": serializer.data})

#New login for both data and token authentication
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user using username and password
    user = authenticate(username=username, password=password)

    if user:
        # If user is authenticated, generate or retrieve a token
        token, created = Token.objects.get_or_create(user=user)
        
        # Serialize the user object to include user data in the response
        serializer = UserSerializer(instance=user)
        
        # Return the token and user data in the response
        return Response({"token": token.key, "user": serializer.data})
    else:
        # If authentication fails, return a 404 Not Found response
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
#===================================================================================

@api_view( ['POST'])
def signUp (request) :
  #Get serializer instance based on the data passed in our request
  serializer = UserSerializer(data=request.data)
  #Check if data valid (username,password & email recieved)
  if serializer.is_valid():
    serializer.save()
    #Retrieve user by username
    user = User.objects.get (username=request. data ['username'] )
    #Save password in a hashed(encoded) format for security reasons
    user.set_password (request.data ['password'])
    user.save()
    #Generate token for frontend
    token = Token.objects.create(user=user)

    #Return user token and data
    return Response({"token": token.key, "user": serializer.data})
  return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view( ['POST'])
def testToken(request):
  return Response ({"message":"This is the doctor's testtoken Api"})