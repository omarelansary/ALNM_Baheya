from rest_framework import serializers 
from django. contrib.auth.models import User

#This is used to map data from Json objects from API to data entries in our database
class UserSerializer (serializers.ModelSerializer):
    class Meta(object) :
        model = User
        fields = ['id', 'username', 'password', 'email']