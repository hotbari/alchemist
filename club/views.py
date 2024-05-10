from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Club
from users.models import CustomUser
from team.models import Team
from coach.models import Coach
from .serializers import (
                    ClubListSerializer,
                    ClubSerializer,
                    CoachSerializer,
                    TeamSerializer,
                    CustomUserSerializer
)


# 클럽 목록 조회 API (회원가입 전용)
class ClubListView(APIView):
    # GET 요청으로 클럽 목록을 조회하는 API
    def get(self, request):
        try:
            # is_deleted=False를 사용하여 삭제되지 않은 클럽만 조회
            clubs = Club.objects.filter(is_deleted=False)
            serializer = ClubListSerializer(clubs, many=True)
            # 성공 시 성공 메세지와 함께 데이터 반환
            return Response({
                'code': '200',
                "message": "클럽 목록 조회 성공",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception:
            # 예외 발생 시 단순한 에러 메세지 반환
            return Response({
                "code": "500",
                "message": "클럽 목록 조회 중 오류발생"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            

# 클럽 상세 정보 조회 API
class ClubDetailView(APIView):
    # GET 요청
    def get(self, request, pk):
        try:
            club = Club.objects.get(pk=pk)
            club_serializer = ClubSerializer(club)

            # 클럽에 속한 코치 정보 가져오기
            coaches = Coach.objects.filter(club=club)
            coach_serializer = CoachSerializer(coaches, many=True)

            # 클럽에 속한 팀 정보 가져오기
            teams = Team.objects.filter(club=club)
            team_serializer = TeamSerializer(teams, many=True)

            # 클럽에 속한 유저 정보 가져오기
            users = CustomUser.objects.filter(club=club)
            user_serializer = CustomUserSerializer(users, many=True)

            # 클럽 정보와 함께 코치, 팀, 유저 정보 포함하여 응답
            response_data = {
                'club': club_serializer.data,
                'coaches': coach_serializer.data,
                'teams': team_serializer.data,
                'users': user_serializer.data
            }
            
            return Response(response_data)
        except Club.DoesNotExist:
            return Response({'error': '해당클럽이 존재하지 않습니다.'}, status=404)