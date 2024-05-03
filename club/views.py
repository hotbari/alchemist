from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Club
from .serializers import ClubSerializer

# class ClubSearchAPIView(APIView): # 클럽 검색할 수 있는 기능
#     def get(self, request):
#         query = request.GET.get('q', '')
#         clubs = Club.objects.filter(name__icontains=query)
#         serializer = ClubSerializer(clubs, many=True)
#         return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Club
from .serializers import ClubSerializer

class ClubListView(APIView):
    # GET 요청으로 클럽 목록을 조회하는 API
    def get(self, request):
        try:
            clubs = Club.objects.all()
            serializer = ClubSerializer(clubs, many=True)
            # 성공 시 성공 메세지와 함께 데이터 반환
            return Response({
                "code": "200",
                "message": "클럽 목록 조회 성공",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception:
            # 예외 발생 시 단순한 에러 메세지 반환
            return Response({
                "code": "500",
                "message": "클럽 목록 조회 중 오류발생"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

