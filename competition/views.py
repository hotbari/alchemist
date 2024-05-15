from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Competition
from applicant.models import Applicant
from .serializers import CompetitionListSerializer, CompetitionSerializer
from applicant.serializers import ApplicantSerializer


class CompetitionListView(APIView):
    """
    대회 리스트
    """
    def get(self, request):
        # 쿼리 파라미터로부터 gender와 type을 받아옵니다.
        gender = request.query_params.get('gender')
        type = request.query_params.get('match_type')

        if gender and type:
            competitions = Competition.objects.filter(match_type__gender=gender, match_type__type=type)
        else:
            competitions = Competition.objects.all()

        serializer = CompetitionListSerializer(competitions, many=True)
        return Response(serializer.data)
    

class CompetitionView(APIView):
    """
    대회 상세보기
    """
    def get(self, request, pk):
        try:
            competition = Competition.objects.get(pk=pk)
            serializer = CompetitionSerializer(competition)
            return Response(serializer.data)
        except Competition.DoesNotExist:
            return Response({'error': 'competition not found'}, status=status.HTTP_404_NOT_FOUND)



# """ """
class CompetitionApplyView(APIView):
    
    def get(self, request, pk):
        try:
            competition = Competition.objects.get(pk=pk)
            serializer = CompetitionSerializer(competition)
            return Response(serializer.data)
        except Competition.DoesNotExist:
            return Response({'error': 'competition not found'}, status=status.HTTP_404_NOT_FOUND)   
        
    def post(self, request, pk):
        competition = Competition.objects.get(pk=pk)
        # if competition.status != 'before':
        #     return Response({"error": "대회 신청이 불가능한 상태입니다."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        if competition.current_applicants < competition.capacity:
            data['is_waiting'] = False
            competition.current_applicants += 1
            competition.save()
        else:
            data['is_waiting'] = True

        serializer = ApplicantSerializer(data=data)
        if serializer.is_valid():
            serializer.save(competition=competition)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)