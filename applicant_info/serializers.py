from rest_framework import serializers
from .models import ApplicantInfo

class ApplicantInfoSerializer(serializers.ModelSerializer):


    class Meta:
        model = ApplicantInfo
        fields = '__all__'