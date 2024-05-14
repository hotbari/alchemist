from rest_framework import serializers
from .models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Applicant
        fields = ['id', 'name', 'phone', 'is_waiting', 'created_at']