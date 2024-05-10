from rest_framework import serializers
from .models import Team

# 팀 모델 All 필드 시리얼라이즈
class TeamSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image_url.image_url', read_only=True)
    
    class Meta:
        model = Team
        fields = '__all__'