# serializers.py
from rest_framework import serializers
from .models import Assessment

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'MRN', 'status','prediction','ground_truth','creation_date','medical_info','doctors'] 
