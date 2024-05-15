# serializers.py
from rest_framework import serializers
from .models import Admin

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'firstName', 'lastName', 'email'] 
