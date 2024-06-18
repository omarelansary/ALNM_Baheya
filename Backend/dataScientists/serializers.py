# serializers.py
from rest_framework import serializers
from .models import DataScientist

class DataScientistSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataScientist
        fields = ['id', 'firstName', 'lastName', 'email'] 
