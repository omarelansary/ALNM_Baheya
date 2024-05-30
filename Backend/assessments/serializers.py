# serializers.py
from rest_framework import serializers
from .models import Assessment

class AssessmentSerializer(serializers.ModelSerializer):
    status_message = serializers.SerializerMethodField()
    class Meta:
        model = Assessment
        fields = ['id', 'MRN', 'status','status_message','prediction','ground_truth','creation_date','medical_info','doctors'] 
    
    def get_status_message(self, obj):
        return obj.get_status_message(obj.status)