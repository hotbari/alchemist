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
class CustomUserSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', '유저 이미지') # 이미지 모델에서 serializser 코드 생성 해줘야함

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ('id', 'name', ' 유저 이미지(유저가 코치가 되기 때문)')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', '팀 이미지')




# 위에서 정의한 Serializer 사용
class ClubDetailSerializer(serializers.ModelSerializer):
    users = CustomUserSerializer(many=True, read_only=True, source='customuser_set') # _set 역참조 기능을 활용하여 클럽에 속한 유저 정보를 가져온다고 보면 될듯!
    coache = CoachSerializer(many=True, read_only=True, source='coach_set')
    team = TeamSerializer(many=True, read_only=True, source='team_set')

    class Meta:
        model = Club
        fields = ('id', 'name', 'description', 'club_image??', 'address', 'phone', 'coaches', 'teams', 'users')
