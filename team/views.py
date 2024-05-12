from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team
from users.models import CustomUser
from .serializers import TeamDetailSerializer
from club.serializers import UserWithTeamInfoSerializer

class TeamDetailView(APIView):
    """
    팀 상세 정보 조회하는 API
    """
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
            team_serializer = TeamDetailSerializer(team)

            # 팀에 속한 유저 정보 가져오기 (코치로 등록된 유저 제외)
            users = CustomUser.objects.filter(team=team)
            user_serializer = UserWithTeamInfoSerializer(users, many=True)

            # 클럽 정보와 함께 코치, 팀, 유저 정보 포함하여 응답
            response_data = {
                'team': team_serializer.data,
                'users': user_serializer.data
            }
            
            return Response(response_data)
        except Team.DoesNotExist:
            return Response({'error': '해당팀이 존재하지 않습니다.'}, status=404)