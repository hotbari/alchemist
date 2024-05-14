from rest_framework import serializers
from .models import MatchType

class MatchTypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = MatchType
        fields = ['gender', 'type']