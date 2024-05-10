from rest_framework import serializers
from .models import Club
from users.models import CustomUser
from coach.models import Coach
from team.models import Team
from image_url.serializers import ImageUrlSerializer




# 전체 클럽 목록 조회 serializer
class ClubListSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)  # ImageUrl 모델에 대한 시리얼라이저를 사용

    class Meta:
        model = Club
        fields = ['id', 'name', 'address', 'image_url']
        






# 클럽 상세정보를 불러오기 위한 Nested Serializer (Nested Serializer : 중첩된 관계를 가진 모델 간의 상호 작용을 지원하는 기능)

class ClubSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)
 
    class Meta:
        model = Club
        fields = ['id', 'address', 'phone', 'name', 'description', 'image_url']
    
        

class CustomUserSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'image_url')


class CoachSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(read_only=True)  # 소속된 클럽의 ID
    user = CustomUserSerializer(read_only=True)  # 코치가 되는 유저 정보

    class Meta:
        model = Coach
        fields = ('id', 'user', 'club')



class TeamSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'image_url')


