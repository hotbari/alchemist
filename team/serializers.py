from rest_framework import serializers
from .models import Team
from users.models import CustomUser
from image_url.serializers import ImageUrlSerializer

class TeamDetailSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)
 
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'image_url']
    
        

# class CustomUserSerializer(serializers.ModelSerializer):
#     image_url = ImageUrlSerializer(read_only=True)
#     team = serializers.SerializerMethodField()  # 사용자의 팀 정보를 커스텀하게 가져오기 위해 사용

#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'image_url', 'team')  # 'team' 필드 추가

#     def get_team(self, obj):
#         # 사용자가 팀에 속해있는 경우
#         if obj.team:
#             # 필요한 팀의 정보(여기서는 id와 name)만을 선택하여 반환
#             return {
#                 'id': obj.team.id,
#                 'name': obj.team.name
#             }
#         # 사용자가 어떤 팀에도 속해있지 않은 경우
#         return None