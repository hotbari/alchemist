from rest_framework import serializers
from .models import MatchType

class CompetitionDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model = MatchType
        fields = '__all__'
