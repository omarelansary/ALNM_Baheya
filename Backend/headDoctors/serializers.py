# serializers.py
from rest_framework import serializers
from .models import headDoctor

class HeadDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = headDoctor
        fields = ['id', 'firstName', 'lastName', 'email'] 
