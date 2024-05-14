from rest_framework import serializers
from .models import Competition
from matchtype.serializers import MatchTypeSerializer
from image_url.serializers import ImageUrlSerializer



''' 대회 부분 '''

class CompetitionSerializer(serializers.ModelSerializer):
    match_type = MatchTypeSerializer(many=True, read_only=True)
    image_url = ImageUrlSerializer(read_only=True)

    class Meta:
        model = Competition
        fields = '__all__'
        
