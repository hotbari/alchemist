from rest_framework import serializers
from .models import Club
from users.models import CustomUser
from coach.models import Coach
from team.models import Team
from image_url.models import ImageUrl
from image_url.serializers import ClubImageSerializer


# 전체 클럽 목록 조회 serializer
class ClubListSerializer(serializers.ModelSerializer):
    # SerializerMethodField: 복잡한 데이터를 직접 계산하거나 다른 소스에서 가져온 데이터를 직렬화에 포함가능함
    club_image = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ('id', 'name', 'address', 'club_image')

    def get_club_image(self, obj):
        # 현재 클럽과 연결된 이미지 중 image_type이 'club'인 이미지만 필터링
        image = ImageUrl.objects.filter(club=obj, image_type='club')
        return ClubImageSerializer(image, many=True).data  # ClubImageSerializer를 사용하여 이미지 시리얼라이징





# 클럽 상세정보를 불러오기 위한 Nested Serializer (Nested Serializer : 중첩된 관계를 가진 모델 간의 상호 작용을 지원하는 기능)
class CustomUserSerializer(serializers.ModelSerializer):
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
